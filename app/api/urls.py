from django.urls import path
from app.api.viewsets import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'projek-data', ProjekDataView, basename='projek')
router.register(r'meaningful_objectives-only', MeaningfulOnlyView, basename='meaningful_objectives-only')
router.register(r'intelligence_experience-only', IntelligenceExperienceOnlyView, basename='intelligence_experience-only')
router.register(r'intelligence_implementation-only', IntelligenceImplementationOnlyView, basename='intelligence_implementation-only')
router.register(r'batasan_pengembangan-only', LimitationOnlyView, basename='batasan_pengembangan-only')
router.register(r'status_realisasi-only', RealizationOnlyView, basename='status_realisasi-only')
router.register(r'perencanaan-only', PlanningOnlyView, basename='perencanaan-only')
router.register(r'status-only', StatusOnlyView, basename='status-only')

urlpatterns = router.urls