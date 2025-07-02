from app.models import *
from .serializers import *
from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound
from rest_framework.viewsets import ModelViewSet

class ProjekDataView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    lookup_field = 'id_projek'
    lookup_url_kwarg = 'id_proyek'
    permission_classes = [AllowAny]

    queryset = ProjekModel.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_serializer_class(self):
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

class MeaningfulOnlyView(viewsets.ModelViewSet):
    queryset = ProjekModel.objects.all()
    serializer_class = MeaningfulOnlySerializer

class IntelligenceExperienceOnlyView(viewsets.ModelViewSet):
    queryset = ProjekModel.objects.all()
    serializer_class = IntelligenceExperienceOnlySerializer

class IntelligenceImplementationOnlyView(viewsets.ModelViewSet):
    queryset = ProjekModel.objects.all()
    serializer_class = IntelligenceImplementationOnlySerializer

class LimitationOnlyView(viewsets.ModelViewSet):
    queryset = ProjekModel.objects.all()
    serializer_class = LimitationOnlySerializer

class RealizationOnlyView(viewsets.ModelViewSet):
    queryset = ProjekModel.objects.all()
    serializer_class = RealizationOnlySerializer

class PlanningOnlyView(viewsets.ModelViewSet):
    queryset = ProjekModel.objects.all()
    serializer_class = PlanningOnlySerializer

class StatusOnlyView(viewsets.ReadOnlyModelViewSet):
    queryset = ProjekModel.objects.all()
    serializer_class = StatusOnlySerializer
