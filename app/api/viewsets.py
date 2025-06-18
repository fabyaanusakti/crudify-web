from app.models import *
from .serializers import *
from rest_framework import viewsets
from rest_framework.exceptions import NotFound

class ProjekDataView(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'id_projek'
    lookup_url_kwarg = 'id_proyek' 
    
    queryset = ProjekModel.objects.all()
    serializer_class = MeaningfulDataSerializer 

    def get_serializer_class(self):
        if self.action == 'retrieve':
            data = self.request.query_params.get('data', 'full')
            return {
                'full': MeaningfulDataSerializer,
                'meaningful_objective': MeaningfulOnlySerializer,
                'intelligence_experience': IntelligenceExperienceOnlySerializer,
                'intelligence_implementation': IntelligenceImplementationOnlySerializer,
                'limitation': LimitationOnlySerializer,
                'realization': RealizationOnlySerializer,
                'planning': PlanningOnlySerializer,
                'status': StatusOnlySerializer,
            }.get(data, MeaningfulDataSerializer)
        return self.serializer_class

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        
        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )
        
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        try:
            obj = queryset.get(**filter_kwargs)
        except ProjekModel.DoesNotExist:
            raise NotFound('Projek tidak ditemukan!')
        
        return obj

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

class StatusOnlyView(viewsets.ReadOnlyModelViewSet):
    queryset = ProjekModel.objects.all()
    serializer_class = StatusOnlySerializer
