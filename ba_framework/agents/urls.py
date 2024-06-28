from django.urls import path
from . import views
from django.urls import include, path
from rest_framework import routers
from . import views

# Creating a default router instance for registering viewsets.
router = routers.DefaultRouter()

# Registering the MetricViewSet with the router. This creates routes for all the standard actions (list, create, retrieve, update, destroy) for the Metric viewset.
router.register(r'metric', views.MetricViewSet, basename='Metric')

# Registering the MetadataViewSet with the router. This creates routes for all the standard actions (list, create, retrieve, update, destroy) for the Metadata viewset.
router.register(r'metadata', views.MetadataViewSet, basename='Metadata')
app_name = 'agents'
urlpatterns = [
    # Mapping the URL "landing" to the index view in the views module. The name "landing" is used for URL reversing.
    path("landing", views.index, name="landing")
]
