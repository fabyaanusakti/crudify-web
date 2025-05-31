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

# ---- Start of Meaningfull Objectives Form ---- #
class ObjectivesForm(forms.ModelForm):
    class Meta:
        model = ObjectiveModels
        fields = {
            'organizational', 
            'leading_indicators', 
            'user_outcomes', 
            'model_properties',
            'date_start',
            'date_end'
        }
        
        labels = {
            'organizational': 'Organizational Objectives',
            'leading_indicators': 'Leading Indicators',
            'user_outcomes': 'User Outcomes',
            'model_properties': 'Model Properties',
            'date_start': 'Tanggal Mulai',
            'date_end': 'Tanggal Selesai'
        }

        widgets = {
            'organizational': forms.Textarea(attrs={
                'class': 'form-control rounded-2 shadow-sm border-1',
                'placeholder': 'Masukan Organizational Objectives',
                'rows': 3
            }),
            'leading_indicators': forms.Textarea(attrs={
                'class': 'form-control rounded-2 shadow-sm border-1',
                'placeholder': 'Masukan Leading Indicators',
                'rows': 3
            }),
            'user_outcomes': forms.Textarea(attrs={
                'class': 'form-control rounded-2 shadow-sm border-1',
                'placeholder': 'Masukan User Outcomes',
                'rows': 3
            }),
            'model_properties': forms.Textarea(attrs={
                'class': 'form-control rounded-2 shadow-sm border-1',
                'placeholder': 'Masukan Model Properties',
                'rows': 3
            }),
            'date_start': forms.DateInput(attrs={
                'class': 'form-control rounded-2 shadow-sm border-1',
                'type': 'date'
            }),
            'date_end': forms.DateInput(attrs={
                'class': 'form-control rounded-2 shadow-sm border-1',
                'type': 'date'
            })
        }
# ---- End of Meaningfull Objectives Form ---- #

# ---- Start of Intelligence Experience Form ---- #
class ExperienceForm(forms.ModelForm):
    class Meta:
        model = ExperienceModels
        fields = {
            'automate',
            'prompt',
            'annotate',
            'organization',
            'system_objectives',
            'minimize_flaws',
            'create_data'
        }

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
            'automate': forms.Textarea(attrs={
                'class': 'form-control rounded-2 shadow-sm border-1',
                'placeholder': 'Masukan automate',
                'rows': 3
            }),
            'prompt': forms.Textarea(attrs={
                'class': 'form-control rounded-2 shadow-sm border-1',
                'placeholder': 'Masukan prompt',
                'rows': 3
            }),
            'annotate': forms.Textarea(attrs={
                'class': 'form-control rounded-2 shadow-sm border-1',
                'placeholder': 'Masukan annotate',
                'rows': 3

            }),
            'organization': forms.Textarea(attrs={
                'class': 'form-control rounded-2 shadow-sm border-1',
                'placeholder': 'Masukan organization',
                'rows': 3
            }),
            'system_objectives': forms.Textarea(attrs={
                'class': 'form-control rounded-2 shadow-sm border-1',
                'placeholder': 'Masukan system objectives',
                'rows': 3
            }),
            'minimize_flaws': forms.Textarea(attrs={
                'class': 'form-control rounded-2 shadow-sm border-1',
                'placeholder': 'Masukan minimize intelligence flaws',
                'rows': 3 
            }),
            'create_data': forms.Textarea(attrs={
                'class': 'form-control rounded-2 shadow-sm border-1',
                'placeholder': 'Masukan data',
                'rows': 3
            })
        }
# ---- End of Intelligence Experience Form ---- #

# ---- Start of Intelligence Implementation Form ---- #
class ImplementationForm(forms.ModelForm):
    class Meta:
        model = ImplementationModels
        fields = {
            'business_process',
            'technology',
            'build_process'
        }

        labels = {
            'business_process': 'Proses bisnis sistem cerdas',
            'technology': 'Teknologi yang akan digunakan',
            'build_process': 'Proses yang akan dibangun'
        }

        widgets = {
            'business_process': forms.Textarea(attrs={
                'class': 'form-control rounded-2 shadow-sm border-1',
                'placeholder':  'Masukan proses bisnis sistem cerdas',
                'rows': 3
            }),
            'technology': forms.Textarea(attrs={
                'class': 'form-control rounded=2 shadow-sm border-1',
                'placeholder': 'Masukan teknologi yang akan digunakan',
                'rows': 3
            }),
            'build_process': forms.Textarea(attrs={
                'class': 'form-control rounded-2 shadow-sm border-1',
                'placeholder': 'Masukan proses yang akan dibangun'
            })
        }
# ---- End of Intelligence Implementation Form ---- #

# ---- Start of Limitation Form ---- #
class LimitationForm(forms.ModelForm):
    class Meta:
        model = LimitationModels
        fields = {
            'limitation'
        }

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
        fields = {
            'realization'
        }

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
        fields = {
            'deployment',
            'maintenance',
            'operating'
        }

        labels = {
            'deployment': 'Pelaksanaan Deployment',
            'maintenance': 'Pemeliharaan Sistem',
            'operating': 'Pelaksanaan Sistem Operasi'
        }

        widgets = {
            'deployment': forms.Textarea(attrs={
                'class': 'form-control rounded-2 shadow-sm border-1',
                'placeholder': 'Masukan pelaksanaan deployment',
                'rows': 3
            }),
            'maintenance': forms.Textarea(attrs={
                'class': 'form-control rounded-2 shadow-sm border-1',
                'placeholder': 'Masukan pemeliharaan sistem',
                'rows': 3
            }),
            'operating': forms.Textarea(attrs={
                'class': 'form-control rounded-2 shadow-sm border-1',
                'placeholder': 'Masukan pelaksanaan sistem operasi',
                'rows': 3
            })
        }
# ---- End of Planning Form ---- #

# ---- Start of Image Upload Form ---- #
# class UploadLogoForm(forms.ModelForm):
#     class Meta:
#         model = UploadLogo
#         fields = {
#             'logo'
#         }

# ---- End of Image Upload Form ---- #