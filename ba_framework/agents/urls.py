from django.urls import path
from . import views
from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'metric', views.MetricViewSet, basename='Metric')
router.register(r'metadata', views.MetadataViewSet, basename='Metadata')


app_name = 'agents'

urlpatterns = [
    path("landing", views.index, name="landing")
]

