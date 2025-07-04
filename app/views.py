import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from app.api.services.project_api_sync import sync_projects
from django.core.files.base import ContentFile
from django.template.loader import get_template
from django.http import JsonResponse
from django.http import HttpResponse
from django.urls import reverse
from django.db.models import Count
from django.views import View
from xhtml2pdf import pisa
from django.conf import settings
from django.contrib import messages
from .forms import *
from .models import *
import base64
import json

# ---- Start of Homepage Views Controller ---- #

def home(request):
    sync_projects()
    chart_labels = ['berlangsung', 'selesai', 'gagal']
    chart_counts = [0, 0, 0]

    if request.user.is_authenticated:
        projects = ProjekModel.objects.all()
        status_data = projects.values('status_projek').annotate(count=Count('status_projek'))
        status_lookup = {item['status_projek']: item['count'] for item in status_data}

        for idx, status in enumerate(chart_labels):
            chart_counts[idx] = status_lookup.get(status, 0)

    context = {
        'chart_labels': json.dumps(chart_labels),
        'chart_counts': json.dumps(chart_counts),
    }

    return render(request, 'app/home.html', context)
# ---- End of Homepage Views Controller ---- #

# ---- Start of Users Views Controller ---- #
def register_view(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Add the backend attribute before login
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return redirect('home')
    else:
        form = CustomRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = CustomLoginForm()
    return render(request, 'users/login.html', {'form': form})


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = CustomUserProfileEditForm(request.POST, request.FILES, instance=request.user)

        image_data = request.POST.get('image_data', None)
        if image_data:
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f'live_capture.{ext}')

            request.user.picture.save(f'live_capture.{ext}', data, save=False)

        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = CustomUserProfileEditForm(instance=request.user)

    return render(request, 'users/profile.html', {'form': form})

# ---- Start of Forgot Password Views Controller ---- #
class ForgotPasswordView(View):
    template_name = 'users/forgot_password.html'

    def get(self, request):
        form = ForgotPasswordForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ForgotPasswordForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {'form': form})

        username_or_email = form.cleaned_data['username_or_email']
        user = User.objects.filter(
            Q(username__iexact=username_or_email) |
            Q(email__iexact=username_or_email)
        ).first()

        return redirect('reset_password', username=user.username)

class ResetPasswordView(View):
    template_name = 'users/reset_password.html'

    def get(self, request, username):
        user = User.objects.filter(username=username).first()
        if not user:
            messages.error(request, "Link reset password tidak valid.")
            return redirect('forgot_password')
        return render(request, self.template_name, {'username': username})

    def post(self, request, username):
        user = User.objects.filter(username=username).first()
        if not user:
            messages.error(request, "Link reset kata sandi tidak valid.")
            return redirect('forgot_password')

        new_password = request.POST.get('new_password1')
        confirm_password = request.POST.get('new_password2')


        if check_password(new_password, user.password):
            messages.error(request, "Kata sandi baru tidak boleh sama dengan kata sandi lama!")
            return render(request, self.template_name, {'username': username})

        if new_password != confirm_password:
            messages.error(request, "Kata sandi tidak cocok!")
            return render(request, self.template_name, {'username': username})

        user.set_password(new_password)
        user.save()
        messages.success(request, "Kata sandi berhasil diubah! Silakan login dengan kata sandi baru Anda.")
        return redirect('login')
# ---- End of Forgot Password Views Controller ---- #

def logout_view(request):
    logout(request)
    return redirect('home')
# ---- End of Users Views Controller ---- #

# ---- Start of Api Setting Controller ---- #
@login_required
def settings_view(request):
    config = AppConfig.load()

    if request.method == 'POST':
        form = AppConfigForm(request.POST, instance=config)
        if form.is_valid():
            form.save()
            messages.success(request, 'Berhasil Diperbarui!')
            return redirect('settings')
    else:
        form = AppConfigForm(instance=config)

    return render(request, 'app/settings.html', {'form': form})

# ---- End of Api Setting Controller ---- #

# ---- Start of Projek Views Controller ---- #
@login_required
def projek_view(request):
    sync_projects()
    projects = ProjekModel.objects.all().prefetch_related(
        'objective',
        'objective__last_edited_by',

        'experience',
        'experience__last_edited_by',

        'implementation',
        'implementation__last_edited_by',

        'limitation',
        'limitation__last_edited_by',

        'realization',
        'realization__last_edited_by',

        'planning',
        'planning__last_edited_by',
    )

    return render(request, 'app/pages/projek/main.html', {
        'projects': projects,
        'status_choices': ProjekModel.STATUS_PROJEK,
        'project': projects.first() if projects.exists() else None
    })

@require_POST
def update_project_status(request, pk):
    try:
        # Get the new status from POST data
        new_status = request.POST.get('status')

        if not new_status:
            messages.error(request, 'Status is required')
            return redirect('projek')

        if new_status not in dict(ProjekModel.STATUS_PROJEK):
            messages.error(request, 'Invalid status')
            return redirect('projek')

        try:
            projek = ProjekModel.objects.get(pk=pk)
        except ProjekModel.DoesNotExist:
            messages.error(request, 'Project not found')
            return redirect('projek')

        projek.status_projek = new_status
        projek.save()

        messages.success(request, 'Status updated successfully')
        return redirect('projek')

    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        return redirect('projek')


@csrf_exempt
@require_POST
def sync_projects_view(request):
    try:
        created, updated, deleted = sync_projects(delete_stale=True)
        return JsonResponse({
            'status': 'success',
            'created': created,
            'updated': updated,
            'deleted': deleted
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'error': str(e)
        }, status=500)
# ---- End of Projek Views Controller ---- #

# ---- Start of Meaningfull Objectives Views Controller ---- #
@login_required
def objectives_view(request):
    user_projects = ProjekModel.objects.all()
    selected_project_id = request.GET.get('project') or request.POST.get('project')

    project = None
    objective = None
    form = None

    if selected_project_id:
        try:
            project = user_projects.get(pk=selected_project_id)
        except ProjekModel.DoesNotExist:
            return redirect('objectives_view')
    elif user_projects.exists():
        project = user_projects.first()

    if project:
        objective, created = ObjectiveModels.objects.get_or_create(project=project)

        if request.method == 'POST':
            form = ObjectivesForm(request.POST, instance=objective)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.last_edited_by = request.user
                obj.save()
                return redirect(f"{reverse('experience_view')}?project={project.id}")
        else:
            form = ObjectivesForm(instance=objective)

    return render(request, 'app/pages/objectives/main.html', {
        'projects': user_projects,
        'project': project,
        'objective': objective,
        'form': form,
        'current_page': 'objectives'
    })
# ---- End of Meaningfull Objectives Views Controller---- #

# ---- Start of Intelligence Experience Views Controller ---- #
@login_required
def experience_view(request):
    user_projects = ProjekModel.objects.all()
    selected_project_id = request.GET.get('project') or request.POST.get('project')

    project = None
    experience = None
    form = None

    if selected_project_id:
        try:
            project = user_projects.get(pk=selected_project_id)
        except ProjekModel.DoesNotExist:
            return redirect('experience_view')
    elif user_projects.exists():
        project = user_projects.first()

    if project:
        experience, created = ExperienceModels.objects.get_or_create(project=project)

        if request.method == 'POST':
            form = ExperienceForm(request.POST, instance=experience)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.last_edited_by = request.user
                obj.save()
                return redirect(f"{reverse('implementation_view')}?project={project.id}")
        else:
            form = ExperienceForm(instance=experience)

    return render(request, 'app/pages/experience/main.html', {
        'projects': user_projects,
        'project': project,
        'experience': experience,
        'form': form,
        'current_page': 'experience'
    })
# ---- End of Intelligence Experience Views Controller ---- #

# ---- Start of Intelligence Implementation Views Controller ---- #
@login_required
def implementation_view(request):
    user_projects = ProjekModel.objects.all()
    selected_project_id = request.GET.get('project') or request.POST.get('project')

    project = None
    implementation = None
    form = None

    if selected_project_id:
        try:
            project = user_projects.get(pk=selected_project_id)
        except ProjekModel.DoesNotExist:
            return redirect('implementation_view')
    elif user_projects.exists():
        project = user_projects.first()

    if project:
        implementation, created = ImplementationModels.objects.get_or_create(project=project)

        if request.method == 'POST':
            form = ImplementationForm(request.POST, instance=implementation)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.last_edited_by = request.user
                obj.save()
                return redirect(f"{reverse('limitation_view')}?project={project.id}")
        else:
            form = ImplementationForm(instance=implementation)

    return render(request, 'app/pages/implementation/main.html', {
        'projects': user_projects,
        'project': project,
        'implementation': implementation,
        'form': form,
        'current_page': 'implementation'
    })
# ---- End of Intelligence Implementation Views Controller ---- #

# ---- Start of Limitation Views Controller ---- #
@login_required
def limitation_view(request):
    user_projects = ProjekModel.objects.all()
    selected_project_id = request.GET.get('project') or request.POST.get('project')

    project = None
    limitation = None
    form = None

    if selected_project_id:
        try:
            project = user_projects.get(pk=selected_project_id)
        except ProjekModel.DoesNotExist:
            return redirect('limitation_view')
    elif user_projects.exists():
        project = user_projects.first()

    if project:
        limitation, created = LimitationModels.objects.get_or_create(project=project)

        if request.method == 'POST':
            form = LimitationForm(request.POST, instance=limitation)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.last_edited_by = request.user
                obj.save()
                return redirect(f"{reverse('realization_view')}?project={project.id}")
        else:
            form = LimitationForm(instance=limitation)

    return render(request, 'app/pages/limitation/main.html', {
        'projects': user_projects,
        'project': project,
        'limitation': limitation,
        'form': form,
        'current_page': 'limitation'
    })
# ---- End of Limitation Views Controller ---- #

# ---- Start of Realization Views Controller ---- #
@login_required
def realization_view(request):
    user_projects = ProjekModel.objects.all()
    selected_project_id = request.GET.get('project') or request.POST.get('project')

    project = None
    realization = None
    form = None

    if selected_project_id:
        try:
            project = user_projects.get(pk=selected_project_id)
        except ProjekModel.DoesNotExist:
            return redirect('realization_view')
    elif user_projects.exists():
        project = user_projects.first()

    if project:
        realization, created = RealizationModels.objects.get_or_create(project=project)

        if request.method == 'POST':
            form = RealizationForm(request.POST, instance=realization)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.last_edited_by = request.user
                obj.save()
                return redirect(f"{reverse('planning_view')}?project={project.id}")
        else:
            form = RealizationForm(instance=realization)

    return render(request, 'app/pages/realization/main.html', {
        'projects': user_projects,
        'project': project,
        'realization': realization,
        'form': form,
        'current_page': 'realization'
    })
# ---- End of Realization Views Controller ---- #

# ---- Start of Planning Views Controller ---- #
@login_required
def planning_view(request):
    user_projects = ProjekModel.objects.all()
    selected_project_id = request.GET.get('project') or request.POST.get('project')

    project = None
    planning = None
    form = None

    if selected_project_id:
        try:
            project = user_projects.get(pk=selected_project_id)
        except ProjekModel.DoesNotExist:
            return redirect('planning_view')
    elif user_projects.exists():
        project = user_projects.first()

    if project:
        planning, created = PlanningModels.objects.get_or_create(project=project)

        if request.method == 'POST':
            form = PlanningForm(request.POST, instance=planning)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.last_edited_by = request.user
                obj.save()
                return redirect('detail_projek', pk=project.id)
        else:
            form = PlanningForm(instance=planning)

    return render(request, 'app/pages/planning/main.html', {
        'projects': user_projects,
        'project': project,
        'planning': planning,
        'form': form,
        'current_page': 'planning'
    })
# ---- End of Planning Views Controller ---- #

# ---- Start of Details Views Controller ---- #
@login_required
def detail_projek_view(request, pk):
    project = get_object_or_404(ProjekModel, pk=pk)

    context = {
        'project': project,
        'objective': getattr(project, 'objective', None),
        'experience': getattr(project, 'experience', None),
        'implementation': getattr(project, 'implementation', None),
        'limitation': getattr(project, 'limitation', None),
        'realization': getattr(project, 'realization', None),
        'planning': getattr(project, 'planning', None)
    }
    return render(request, 'app/pages/details/main.html', context)

def download_pdf(request, pk):
    project = get_object_or_404(ProjekModel, pk=pk)

    context = {
        'project': project,
        'objective': getattr(project, 'objective', None),
        'experience': getattr(project, 'experience', None),
        'implementation': getattr(project, 'implementation', None),
        'limitation': getattr(project, 'limitation', None),
        'realization': getattr(project, 'realization', None),
        'planning': getattr(project, 'planning', None)
    }

    template_path = 'layout/pdf_template.html'
    template = get_template(template_path)
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')

    filename = f"{project.nama_projek}_documentation.pdf".replace(" ", "_")
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    pisa_status = pisa.CreatePDF(
        html,
        dest=response,
        encoding='UTF-8',
        link_callback=lambda uri, _: os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ''))
    )

    if pisa_status.err:
        return HttpResponse('We had some errors generating the PDF. Please try again later.')

    return response

# ---- Start of Details Views Controller ---- #


