from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# ---- Start of User Profile Models ---- #
class CustomUserProfileModels(AbstractUser):
    picture = models.ImageField(
        upload_to='images/', 
        default='images/default.png', 
        verbose_name='Foto Anggota', 
        blank=True, 
        null=True
    )
    
    def __str__(self):
        return self.username
# ---- End of User Profile Models ---- #

# ---- Start of Project Model Models ---- #
class ProjekModel(models.Model):
    """Model representing a project"""
    
    id_projek = models.IntegerField(unique=True)
    nama_projek = models.CharField(max_length=255)
    deskripsi = models.TextField(blank=True)
    lokasi = models.CharField(max_length=255, blank=True)
    tanggal_mulai = models.DateField()
    tanggal_selesai = models.DateField()
    supervisor = models.CharField(max_length=255, blank=True)
    status_projek = models.CharField(max_length=20)
    last_updated = models.DateTimeField(auto_now=True)
    last_updated_source = models.CharField(
        max_length=10,
        choices=[('API_PUSH', 'Push'), ('API_PULL', 'Pull')],
        default='API_PULL'
    )

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        ordering = ['-tanggal_mulai']

    def __str__(self):
        return self.nama_projek
# ---- End of Project Model Models ---- #

# ---- Start of Meaningful Objectives Models ---- #
class ObjectiveModels(models.Model):  
    project = models.OneToOneField(
        ProjekModel,
        on_delete=models.CASCADE,
        related_name='objective',
        verbose_name='Related Project'
    )

    organizational = models.TextField(verbose_name='Organizational Objectives')
    leading_indicators = models.TextField(verbose_name='Leading Indicators')
    user_outcomes = models.TextField(verbose_name='User Outcomes')
    model_properties = models.TextField(verbose_name='Model Properties')
    date_start = models.DateField(null=True, blank=True, verbose_name='Tanggal Mulai')
    date_end = models.DateField(null=True, blank=True, verbose_name='Tanggal Selesai')

    class Meta:
        verbose_name = "Meaningful Objective"
        verbose_name_plural = "Meaningful Objectives"
# ---- End of Meaningful Objectives Models ---- #

# ---- Start of Intelligence Experience Models ---- #
class ExperienceModels(models.Model):  
    project = models.OneToOneField(
        ProjekModel,
        on_delete=models.CASCADE,
        related_name='experience',
        verbose_name='Related Project'
    )

    automate = models.TextField(verbose_name='Automate')
    prompt = models.TextField(verbose_name='Prompt')
    annotate = models.TextField(verbose_name='Annotate')
    organization = models.TextField(verbose_name='Organization')
    system_objectives = models.TextField(verbose_name='System Objectives')
    minimize_flaws = models.TextField(verbose_name='Minimize Intelligence Flaws')
    create_data = models.TextField(verbose_name='Create data to grow')

    class Meta:
        verbose_name = "Intelligence Experience"
        verbose_name_plural = "Intelligence Experiences"
# ---- End of Intelligence Experience Models ---- #

# ---- Start of Intelligence Implementation Models ---- #
class ImplementationModels(models.Model):  
    project = models.OneToOneField(
        ProjekModel,
        on_delete=models.CASCADE,
        related_name='implementation',
        verbose_name='Related Project'
    )

    business_process = models.TextField(verbose_name='Business Process')
    technology = models.TextField(verbose_name='Used Technology')
    build_process = models.TextField(verbose_name='Built Process')

    class Meta:
        verbose_name = "Intelligence Implementation"
        verbose_name_plural = "Intelligence Implementations"
# ---- End of Intelligence Implementation Models ---- #

# ---- Start of Limitation Models ---- #
class LimitationModels(models.Model):  
    project = models.OneToOneField(
        ProjekModel,
        on_delete=models.CASCADE,
        related_name='limitation',
        verbose_name='Related Project'
    )
    
    limitation = models.TextField(verbose_name='Limitation')

    class Meta:
        verbose_name = "Limitation"
        verbose_name_plural = "Limitations"
# ---- End of Limitation Models ---- #

# ---- Start of Realization Models ---- #
class RealizationModels(models.Model):
    project = models.OneToOneField(
        ProjekModel,
        on_delete=models.CASCADE,
        related_name='realization',
        verbose_name='Related Project'
    )

    realization = models.TextField(verbose_name='Realization')

    class Meta:
        verbose_name = 'Realization'
        verbose_name_plural = 'Realizations'
# ---- End of Realization Models ---- #

# ---- Start of Planning Models ---- #
class PlanningModels(models.Model):
    project = models.OneToOneField(
        ProjekModel,
        on_delete=models.CASCADE,
        related_name='planning',
        verbose_name='Related Project'
    )

    deployment = models.TextField(verbose_name='Deployment')
    maintenance = models.TextField(verbose_name='Maintenance')
    operating = models.TextField(verbose_name='Operating System')

    class Meta:
        verbose_name = 'Planning'
        verbose_name_plural = 'Plannings'
# ---- End of Planning Models ---- #