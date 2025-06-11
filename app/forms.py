from django import forms
from .models import *
from .forms import *
from django.contrib.auth.forms import *
from django.contrib.auth import get_user_model


# ---- Start of User Login & Register ---- #
User = get_user_model()

class CustomRegisterForm(UserCreationForm):
    username = forms.CharField(
        required=True,
        label='Username',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Masukan Username'
        }),
    )

    email = forms.EmailField(
        required=True,
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Masukkan Email'
        }),
    )

    password1 = forms.CharField(
        required=True,
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Masukan Password'
        }),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'password2' in self.fields:
            del self.fields['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={
            'name': 'username',
            'type': 'text',
            'class': 'form-control', 
            'placeholder': 'Masukkan Username',
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