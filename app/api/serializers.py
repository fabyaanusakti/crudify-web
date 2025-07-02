from app.models import *
from rest_framework import serializers, viewsets

# --- Start of Objective Serializer --- #
class ObjectiveSerializer(serializers.ModelSerializer):
    organizational = serializers.CharField(required=False, allow_blank=True)
    leading_indicators = serializers.CharField(required=False, allow_blank=True)
    user_outcomes = serializers.CharField(required=False, allow_blank=True)
    model_properties = serializers.CharField(required=False, allow_blank=True)
    status = serializers.CharField(required=False)

    class Meta:
        model = ObjectiveModels
        exclude = ['project', 'id', 'last_edited', 'last_edited_by']

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        request = self.context.get('request')
        if request and request.user.is_authenticated:
            instance.last_edited_by = request.user

        instance.save()
        return instance
# --- End of Objective Serializer --- #


# --- Start of Experience Serializer --- #
class ExperienceSerializer(serializers.ModelSerializer):
    automate = serializers.CharField(required=False, allow_blank=True)
    prompt = serializers.CharField(required=False, allow_blank=True)
    annotate = serializers.CharField(required=False, allow_blank=True)
    organization = serializers.CharField(required=False, allow_blank=True)
    system_objectives = serializers.CharField(required=False, allow_blank=True)
    minimize_flaws = serializers.CharField(required=False, allow_blank=True)
    create_data = serializers.CharField(required=False, allow_blank=True)
    status = serializers.CharField(required=False)

    class Meta:
        model = ExperienceModels
        exclude = ['project', 'id', 'last_edited', 'last_edited_by']

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        request = self.context.get('request')
        if request and request.user.is_authenticated:
            instance.last_edited_by = request.user

        instance.save()
        return instance
# --- End of Experience Serializer --- #


# --- Start of Implementation Serializer --- #
class ImplementationSerializer(serializers.ModelSerializer):
    business_process = serializers.CharField(required=False, allow_blank=True)
    technology = serializers.CharField(required=False, allow_blank=True)
    build_process = serializers.CharField(required=False, allow_blank=True)
    status = serializers.CharField(required=False)

    class Meta:
        model = ImplementationModels
        exclude = ['project', 'id', 'last_edited', 'last_edited_by']

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        request = self.context.get('request')
        if request and request.user.is_authenticated:
            instance.last_edited_by = request.user

        instance.save()
        return instance
# --- End of Implementation Serializer --- #


# --- Start of Limitation Serializer --- #
class LimitationSerializer(serializers.ModelSerializer):
    limitation = serializers.CharField(required=False, allow_blank=True)
    status = serializers.CharField(required=False)

    class Meta:
        model = LimitationModels
        exclude = ['project', 'id', 'last_edited', 'last_edited_by']

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        request = self.context.get('request')
        if request and request.user.is_authenticated:
            instance.last_edited_by = request.user

        instance.save()
        return instance
# --- End of Limitation Serializer --- #


# --- Start of Realization Serializer --- #
class RealizationSerializer(serializers.ModelSerializer):
    realization = serializers.CharField(required=False, allow_blank=True)
    status = serializers.CharField(required=False)

    class Meta:
        model = RealizationModels
        exclude = ['project', 'id', 'last_edited', 'last_edited_by']

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        request = self.context.get('request')
        if request and request.user.is_authenticated:
            instance.last_edited_by = request.user

        instance.save()
        return instance
# --- End of Realization Serializer --- #


# --- Start of Planning Serializer --- #
class PlanningSerializer(serializers.ModelSerializer):
    deployment = serializers.CharField(required=False, allow_blank=True)
    maintenance = serializers.CharField(required=False, allow_blank=True)
    operating = serializers.CharField(required=False, allow_blank=True)
    status = serializers.CharField(required=False)

    class Meta:
        model = PlanningModels
        exclude = ['project', 'id', 'last_edited', 'last_edited_by']

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        request = self.context.get('request')
        if request and request.user.is_authenticated:
            instance.last_edited_by = request.user

        instance.save()
        return instance
# --- End of Planning Serializer --- #


class MeaningfulDataSerializer(serializers.ModelSerializer):
    meaningful_objectives = serializers.SerializerMethodField()
    intelligence_experience = serializers.SerializerMethodField()
    intelligence_implementation = serializers.SerializerMethodField()
    batasan_pengembangan = serializers.SerializerMethodField()
    status_realisasi = serializers.SerializerMethodField()
    perencanaan = serializers.SerializerMethodField()

    class Meta:
        model = ProjekModel
        fields = [
            'id_projek',
            'nama_projek',
            'meaningful_objectives',
            'intelligence_experience',
            'intelligence_implementation',
            'batasan_pengembangan',
            'status_realisasi',
            'perencanaan'
        ]
        read_only_fields = ['id_projek', 'nama_projek']

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

    def update(self, instance, validated_data):
        instance.nama_projek = validated_data.get('nama_projek', instance.nama_projek)
        instance.save()
        return instance
# --- End of Meaningful Data Serialization --- #

# --- Start of Meaningful only Serialization --- #
class MeaningfulOnlySerializer(serializers.ModelSerializer):
    meaningful_objectives = ObjectiveSerializer(source='objective')

    class Meta:
        model = ProjekModel
        fields = ['id_projek', 'nama_projek', 'meaningful_objectives']
        read_only_fields = ['id_projek', 'nama_projek', 'status']

    def update(self, instance, validated_data):
        objective_data = validated_data.pop('objective', None)
        instance = super().update(instance, validated_data)

        if objective_data:
            if hasattr(instance, 'objective'):
                ObjectiveSerializer().update(instance.objective, objective_data)
            else:
                ObjectiveModels.objects.create(project=instance, **objective_data)

        return instance
# --- End of Meaningful only Serialization --- #

# --- Start of Intelligence Experience only Serialization --- #
class IntelligenceExperienceOnlySerializer(serializers.ModelSerializer):
    intelligence_experience = ExperienceSerializer(source='experience')

    class Meta:
        model = ProjekModel
        fields = ['id_projek', 'nama_projek', 'intelligence_experience']
        read_only_fields = ['id_projek', 'nama_projek', 'status']

    def update(self, instance, validated_data):
        experience_data = validated_data.pop('experience', None)
        instance = super().update(instance, validated_data)

        if experience_data:
            if hasattr(instance, 'experience'):
                ExperienceSerializer().update(instance.experience, experience_data)
            else:
                ExperienceModels.objects.create(project=instance, **experience_data)

        return instance
# --- End of Intelligence Experience only Serialization --- #
class IntelligenceImplementationOnlySerializer(serializers.ModelSerializer):
    intelligence_implementation = ImplementationSerializer(source='implementation')

    class Meta:
        model = ProjekModel
        fields = ['id_projek', 'nama_projek', 'intelligence_implementation']
        read_only_fields = ['id_projek', 'nama_projek', 'status']

    def update(self, instance, validated_data):
        implementation_data = validated_data.pop('implementation', None)
        instance = super().update(instance, validated_data)

        if implementation_data:
            if hasattr(instance, 'implementation'):
                ImplementationSerializer().update(instance.implementation, implementation_data)
            else:
                ImplementationModels.objects.create(project=instance, **implementation_data)

        return instance
# --- Start of Intelligence Implementation only Serialization --- #

# --- Start of Limitation only Serialization --- #
class LimitationOnlySerializer(serializers.ModelSerializer):
    batasan_pengembangan = LimitationSerializer(source='limitation')

    class Meta:
        model = ProjekModel
        fields = ['id_projek', 'nama_projek', 'batasan_pengembangan']
        read_only_fields = ['id_projek', 'nama_projek', 'status']

    def update(self, instance, validated_data):
        limitation_data = validated_data.pop('limitation', None)
        instance = super().update(instance, validated_data)

        if limitation_data:
            if hasattr(instance, 'limitation'):
                LimitationSerializer().update(instance.limitation, limitation_data)
            else:
                LimitationModels.objects.create(project=instance, **limitation_data)

        return instance

# --- End of Limitation only Serialization --- #

# --- Start of Realization only Serialization --- #
class RealizationOnlySerializer(serializers.ModelSerializer):
    status_realisasi = RealizationSerializer(source='realization')

    class Meta:
        model = ProjekModel
        fields = ['id_projek', 'nama_projek', 'status_realisasi']
        read_only_fields = ['id_projek', 'nama_projek', 'status']

    def update(self, instance, validated_data):
        realization_data = validated_data.pop('realization', None)
        instance = super().update(instance, validated_data)

        if realization_data:
            if hasattr(instance, 'realization'):
                RealizationSerializer().update(instance.realization, realization_data)
            else:
                RealizationModels.objects.create(project=instance, **realization_data)

        return instance
# --- End of Realization only Serialization --- #

# --- Start of Planning only Serialization --- #
class PlanningOnlySerializer(serializers.ModelSerializer):
    perencanaan = PlanningSerializer(source='planning')

    class Meta:
        model = ProjekModel
        fields = ['id_projek', 'nama_projek', 'perencanaan']
        read_only_fields = ['id_projek', 'nama_projek', 'status']

    def update(self, instance, validated_data):
        planning_data = validated_data.pop('planning', None)
        instance = super().update(instance, validated_data)

        if planning_data:
            if hasattr(instance, 'planning'):
                PlanningSerializer().update(instance.planning, planning_data)
            else:
                PlanningModels.objects.create(project=instance, **planning_data)

        return instance
# --- Start of Planning only Serialization --- #

# --- Start of Status only Serialization --- #
class StatusOnlySerializer(serializers.Serializer):
    id = serializers.IntegerField(source='id_projek')
    nama_proyek = serializers.CharField(source='nama_projek')
    status = serializers.CharField(source='status_projek')
# --- End of Status only Serialization --- #
