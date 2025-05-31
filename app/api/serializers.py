from rest_framework import serializers
from app.models import ProjekModels
from app.api.utils.parse import parse_date        

class ProjekPushSerializer(serializers.Serializer):
    id              = serializers.IntegerField()          
    nama_projek     = serializers.CharField(max_length=255)
    deskripsi       = serializers.CharField(allow_blank=True, required=False)
    lokasi          = serializers.CharField(max_length=255, allow_blank=True, required=False)
    tanggal_mulai   = serializers.DateField()
    tanggal_selesai = serializers.DateField()
    supervisor      = serializers.CharField(max_length=255, allow_blank=True, required=False)
    status_projek   = serializers.ChoiceField(choices=[c[0] for c in ProjekModels.STATUS_PROJEK])

    def create_or_update(self):
        """Upsert helper: returns obj, created_bool"""
        validated = self.validated_data
        obj, created = ProjekModels.objects.update_or_create(
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
