from django import forms
from .models import *
from .forms import *
from django.db.models import Q
from django.contrib.auth.forms import *
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate


# ---- Start of User Login & Register ---- #
User = get_user_model()

class CustomRegisterForm(UserCreationForm):
    username = forms.CharField(
        required=True,
        label='Username',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Masukkan Username',
        }),
    )

    email = forms.EmailField(
        required=True,
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Masukkan Email',
        }),
    )

    password1 = forms.CharField(
        required=True,
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Masukkan Password',
            'id': 'password1'
        }),
    )

    password2 = forms.CharField(
        required=True,
        label='Konfirmasi Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ulangi Password',
            'id': 'password2'
        }),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError(_("Username sudah digunakan."))
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError(_("Email sudah digunakan."))
        return email

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise ValidationError(_("Password harus minimal 8 karakter."))
        # if not re.search(r'[A-Z]', password):
        #     raise ValidationError(_("Password harus mengandung huruf kapital."))
        # if not re.search(r'[a-z]', password):
        #     raise ValidationError(_("Password harus mengandung huruf kecil."))
        # if not re.search(r'[0-9]', password):
        #     raise ValidationError(_("Password harus mengandung angka."))
        return password

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(_("Password dan konfirmasi tidak cocok."))
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
class CustomLoginForm(forms.Form):
    username = forms.CharField(
        label="Username atau Email",
        widget=forms.TextInput(attrs={
            'name': 'username',
            'type': 'text',
            'class': 'form-control',
            'placeholder': 'Masukkan Username atau Email',
            'autofocus': True,
        }),
        strip=False,
    )

    password = forms.CharField(
        label="Kata Sandi",
        widget=forms.PasswordInput(attrs={
            'name': 'password',
            'type': 'password',
            'class': 'form-control',
            'placeholder': 'Masukkan Kata Sandi',
            'id': 'password',
        }),
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        username_or_email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if not username_or_email or not password:
            raise forms.ValidationError(_("Semua kolom wajib diisi."))

        # Check if user exists
        user_qs = User.objects.filter(
            Q(username__iexact=username_or_email) | Q(email__iexact=username_or_email)
        )
        if not user_qs.exists():
            raise forms.ValidationError(_("Akun dengan username/email ini tidak ditemukan."))

        # Try authenticating with username first, then email
        self.user_cache = authenticate(
            self.request,
            username=username_or_email,
            password=password
        )
        
        if self.user_cache is None:
            # If username auth failed, try email auth
            try:
                user = User.objects.get(email__iexact=username_or_email)
                self.user_cache = authenticate(
                    self.request,
                    username=user.username,
                    password=password
                )
            except User.DoesNotExist:
                pass

        if self.user_cache is None:
            raise forms.ValidationError(_("Kata sandi salah."))

        # Set the backend explicitly
        self.user_cache.backend = 'django.contrib.auth.backends.ModelBackend'  # or your custom backend
        
        self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data
    
    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in.
        """
        if not user.is_active:
            raise forms.ValidationError(
                _("Akun ini tidak aktif."),
                code='inactive',
            )
        
        if user.has_usable_password() is False:
            raise forms.ValidationError(
                _("Akun ini tidak dapat login menggunakan password."),
                code='no_password',
            )

    def get_user(self):
        return self.user_cache

class CustomUserProfileEditForm(UserChangeForm):
    password = None
    
    email = forms.EmailField(
        required=True,
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Masukkan Email'
        }),
    )

    picture = forms.ImageField(
        required=False,
        label='Unggah Foto',
        widget=forms.FileInput(attrs={
            'class': 'form-control rounded-2 shadow-sm border-1',
        }),
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'picture')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Masukkan Username'
            })
        }
# ---- End of  user Login & Register ---- #

# ---- Start of Api Endpoint Form ---- #
class AppConfigForm(forms.ModelForm):
    class Meta:
        model = AppConfig
        fields = '__all__'
        labels = {
            'projek_api_endpoint': 'API Projek',
            'meaningful_data_endpoint': 'API Meaningful Data',
            'meaningful_objectives_endpoint': 'API Meaningful Objectives',
            'intelligence_experience_endpoint': 'API Intelligence Experience',
            'intelligence_implementation_endpoint': 'API Intelligence Implementation',
            'limitation_endpoint': 'API Batasan Pengembangan',
            'realization_status_endpoint': 'API Status Realisasi',
            'planning_endpoint': 'API Perencanaan',
            'status_endpoint': 'API Status'
        }
        widgets = {
            field: forms.URLInput(attrs={
                'class': 'form-control rounded-2 shadow-sm border-1 mb-3',
                'placeholder': f'Masukan Alamat {label}'
            }) for field, label in labels.items()
        }
# ---- End of Api Endpoint Form ---- #

# ---- Start of Meaningfull Objectives Form ---- #
class ObjectivesForm(forms.ModelForm):
    class Meta:
        model = ObjectiveModels
        fields = '__all__'
        exclude = ['project'] 
        labels = {
            'organizational': 'Organizational Objectives',
            'leading_indicators': 'Leading Indicators',
            'user_outcomes': 'User Outcomes',
            'model_properties': 'Model Properties',
        }

        widgets = {
            field: forms.Textarea(attrs={
                'class': 'form-control rounded-2 shadow-sm border-1',
                'placeholder': f'Masukan {label}'
            }) for field, label in labels.items()
        }
# ---- End of Meaningfull Objectives Form ---- #

# ---- Start of Intelligence Experience Form ---- #
class ExperienceForm(forms.ModelForm):
    class Meta:
        model = ExperienceModels
        fields = '__all__'
        exclude = ['project'] 
        labels = {
            'automate': 'Automate',
            'prompt': 'Prompt',
            'annotate': 'Annotate',
            'organization': 'Organization',
            'system_objectives': 'Achieve System Objectives',
            'minimize_flaws': 'Minimize Intelligence Flaws',
            'create_data': 'Create Data to Grow'
        }

        widgets = {
            field: forms.Textarea(attrs={
                'class': 'form-control rounded-2 shadow-sm border-1',
                'placeholder': f'Masukan {label}'
            }) for field, label in labels.items()
        }
# ---- End of Intelligence Experience Form ---- #

# ---- Start of Intelligence Implementation Form ---- #
class ImplementationForm(forms.ModelForm):
    class Meta:
        model = ImplementationModels
        fields = '__all__'
        exclude = ['project'] 
        labels = {
            'business_process': 'Proses bisnis sistem cerdas',
            'technology': 'Teknologi yang akan digunakan',
            'build_process': 'Proses yang akan dibangun'
        }

        widgets = {
            field: forms.Textarea(attrs={
                'class': 'form-control rounded-2 shadow-sm border-1',
                'placeholder': f'Masukan {label}'
            }) for field, label in labels.items()
        }
# ---- End of Intelligence Implementation Form ---- #

# ---- Start of Limitation Form ---- #
class LimitationForm(forms.ModelForm):
    class Meta:
        model = LimitationModels
        fields = '__all__'
        exclude = ['project'] 
        labels = {
            'limitation': 'Batasan Pengembangan'
        }

        limitation = forms.CharField(
            widget=forms.Textarea(attrs={             
                'class': 'form-control rounded-2 shadow-sm border-1',
                'rows': 3,
                'cols': 60
    })
)
# ---- End of Limitation Form ---- #

# ---- Start of Realization Form ---- #
class RealizationForm(forms.ModelForm):
    class Meta:
        model = RealizationModels
        fields = '__all__'
        exclude = ['project'] 
        labels = {
            'realization': 'Status Realisasi'
        }

        realization = forms.CharField(
            widget=forms.Textarea(attrs={
                'class': 'form-control rounded-2 shadow-sm border-1',
                'rows': 3,
                'cols': 60
            })
        )
# ---- End of Realization Form ---- #

# ---- Start of Planning Form ---- #
class PlanningForm(forms.ModelForm):
    class Meta:
        model = PlanningModels
        fields = '__all__'
        exclude = ['project'] 
        labels = {
            'deployment': 'Pelaksanaan Deployment',
            'maintenance': 'Pemeliharaan Sistem',
            'operating': 'Pelaksanaan Sistem Operasi'
        }

        widgets = {
            field: forms.Textarea(attrs={
                'class': 'form-control rounded-2 shadow-sm border-1',
                'placeholder': f'Masukan {label}'
            }) for field, label in labels.items()
        }
# ---- End of Planning Form ---- #