from app.models import *
from .serializers import *
from rest_framework import viewsets

class MeaningfulDataView(viewsets.ReadOnlyModelViewSet):
    queryset = ProjekModel.objects.all()
    serializer_class = MeaningfulDataSerializer

class MeaningfulOnlyView(viewsets.ReadOnlyModelViewSet):
    queryset = ProjekModel.objects.all()
    serializer_class = MeaningfulOnlySerializer

class IntelligenceExperienceOnlyView(viewsets.ReadOnlyModelViewSet):
    queryset = ProjekModel.objects.all()
    serializer_class = IntelligenceExperienceOnlySerializer

class IntelligenceImplementationOnlyView(viewsets.ReadOnlyModelViewSet):
    queryset = ProjekModel.objects.all()
    serializer_class = IntelligenceImplementationOnlySerializer

class LimitationOnlyView(viewsets.ReadOnlyModelViewSet):
    queryset = ProjekModel.objects.all()
    serializer_class = LimitationOnlySerializer

class RealizationOnlyView(viewsets.ReadOnlyModelViewSet):
    queryset = ProjekModel.objects.all()
    serializer_class = RealizationOnlySerializer

class PlanningOnlyView(viewsets.ReadOnlyModelViewSet):
    queryset = ProjekModel.objects.all()
    serializer_class = PlanningOnlySerializer