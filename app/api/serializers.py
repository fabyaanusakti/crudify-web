from rest_framework import serializers
from app.models import *      

# --- Start of ProjekPushSerializer --- #
class ProjekPushSerializer(serializers.Serializer):
    id              = serializers.IntegerField()          
    nama_projek     = serializers.CharField(max_length=255)
    deskripsi       = serializers.CharField(allow_blank=True, required=False)
    lokasi          = serializers.CharField(max_length=255, allow_blank=True, required=False)
    tanggal_mulai   = serializers.DateField()
    tanggal_selesai = serializers.DateField()
    supervisor      = serializers.CharField(max_length=255, allow_blank=True, required=False)
    status_projek   = serializers.ChoiceField(choices=[c[0] for c in ProjekModel.STATUS_PROJEK])

    def create_or_update(self):
        validated = self.validated_data
        obj, created = ProjekModel.objects.update_or_create(
            id_projek=validated['id'],
            defaults={
                'nama_projek'    : validated['nama_projek'],
                'deskripsi'      : validated.get('deskripsi', ''),
                'lokasi'         : validated.get('lokasi', ''),
                'tanggal_mulai'  : validated['tanggal_mulai'],
                'tanggal_selesai': validated['tanggal_selesai'],
                'supervisor'     : validated.get('supervisor', ''),
                'status_projek'  : validated['status_projek'],
            }
        )
        return obj, created
# --- End of ProjekPushSerializer --- #


# --- Start of Meaningful Data Serialization --- #    
class ObjectiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectiveModels
        exclude = ['project', 'id']
class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperienceModels
        exclude = ['project', 'id']
class ImplementationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImplementationModels
        exclude = ['project', 'id']
class LimitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LimitationModels
        exclude = ['project', 'id']
class RealizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RealizationModels
        exclude = ['project', 'id']
class PlanningSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanningModels
        exclude = ['project', 'id']
# --- End of Meaningful Data Serialization --- #   

class MeaningfulDataSerializer(serializers.Serializer):
    id_proyek = serializers.IntegerField(source='id_projek')
    nama_proyek = serializers.CharField(source='nama_projek')
    meaningful_objectives = serializers.SerializerMethodField()
    intelligence_experience = serializers.SerializerMethodField()
    intelligence_implementation = serializers.SerializerMethodField()
    batasan_pengembangan = serializers.SerializerMethodField()
    status_realisasi = serializers.SerializerMethodField()
    perencanaan = serializers.SerializerMethodField()

    def get_meaningful_objectives(self, obj):
        if hasattr(obj, 'objective'):
            return ObjectiveSerializer(obj.objective).data
        return None
    def get_intelligence_experience(self, obj):
        if hasattr(obj, 'experience'):
            return ExperienceSerializer(obj.experience).data
        return None
    def get_intelligence_implementation(self, obj):
        if hasattr(obj, 'implementation'):
            return ImplementationSerializer(obj.implementation).data
        return None
    def get_batasan_pengembangan(self, obj):
        if hasattr(obj, 'limitation'):
            return LimitationSerializer(obj.limitation).data
        return None
    def get_status_realisasi(self, obj):
        if hasattr(obj, 'realization'):
            return RealizationSerializer(obj.realization).data
        return None
    def get_perencanaan(self, obj):
        if hasattr(obj, 'planning'):
            return PlanningSerializer(obj.planning).data
        return None
# --- End of Meaningful Data Serialization --- # 

# --- Start of Meaningful only Serialization --- #
class MeaningfulOnlySerializer(serializers.Serializer):
    id_proyek = serializers.IntegerField(source='id_projek')
    nama_proyek = serializers.CharField(source='nama_projek')
    meaningful_objectives = serializers.SerializerMethodField() 
    def get_meaningful_objectives(self, obj):
        if hasattr(obj, 'objective'):
            return ObjectiveSerializer(obj.objective).data
        return None
# --- End of Meaningful only Serialization --- # 

# --- Start of Intelligence Experience only Serialization --- #
class IntelligenceExperienceOnlySerializer(serializers.Serializer):
    id_proyek = serializers.IntegerField(source='id_projek')
    nama_proyek = serializers.CharField(source='nama_projek')
    intelligence_experience = serializers.SerializerMethodField()
    def get_intelligence_experience(self, obj):
        if hasattr(obj, 'experience'):
            return ExperienceSerializer(obj.expeience).data
        return None 
# --- End of Intelligence Experience only Serialization --- # 
class IntelligenceImplementationOnlySerializer(serializers.Serializer):
    id_proyek = serializers.IntegerField(source='id_projek')
    nama_proyek = serializers.CharField(source='nama_projek')
    intelligence_implementation = serializers.SerializerMethodField()
    def get_intelligence_implementation(self, obj):
        if hasattr(obj, 'implementation'):
            return ImplementationSerializer(obj.implementation).data
        return None
# --- Start of Intelligence Implementation only Serialization --- # 

# --- Start of Limitation only Serialization --- # 
class LimitationOnlySerializer(serializers.Serializer):
    id_proyek = serializers.IntegerField(source='id_projek')
    nama_proyek = serializers.CharField(source='nama_projek')
    batasan_pengembangan = serializers.SerializerMethodField()
    def get_batasan_pengembangan(self, obj):
        if hasattr(obj, 'limitation'):
            return LimitationSerializer(obj.limitation).data
        return None
# --- End of Limitation only Serialization --- #

# --- Start of Realization only Serialization --- #
class RealizationOnlySerializer(serializers.Serializer):
    id_proyek = serializers.IntegerField(source='id_projek')
    nama_proyek = serializers.CharField(source='nama_projek')
    status_realisasi = serializers.SerializerMethodField()
    def get_status_realisasi(self, obj):
        if hasattr(obj, 'realization'):
            return RealizationSerializer(obj.realization).data
        return None
# --- End of Realization only Serialization --- #

# --- Start of Planning only Serialization --- #
class PlanningOnlySerializer(serializers.Serializer):
    id_proyek = serializers.IntegerField(source='id_projek')
    nama_proyek = serializers.CharField(source='nama_projek')
    perencanaan = serializers.SerializerMethodField()
    def get_perencanaan(self, obj):
        if hasattr(obj, 'planning'):
            return PlanningSerializer(obj.planning).data
        return None
# --- Start of Planning only Serialization --- #