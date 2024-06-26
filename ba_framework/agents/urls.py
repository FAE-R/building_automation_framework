# Importing the path function from Django's urls module to define URL patterns.
from django.urls import path

# Importing views from the current package to link URLs to view functions.
from . import views

# Importing the include function from Django's urls module to include other URL configurations.
from django.urls import include, path

# Importing the routers module from Django Rest Framework to create and register viewsets with URL routes.
from rest_framework import routers

# Importing views again from the current package (duplicate import, can be removed).
from . import views

# Creating a default router instance for registering viewsets.
router = routers.DefaultRouter()

# Registering the MetricViewSet with the router. This creates routes for all the standard actions (list, create, retrieve, update, destroy) for the Metric viewset.
router.register(r'metric', views.MetricViewSet, basename='Metric')

# Registering the MetadataViewSet with the router. This creates routes for all the standard actions (list, create, retrieve, update, destroy) for the Metadata viewset.
router.register(r'metadata', views.MetadataViewSet, basename='Metadata')

# Defining the application namespace for the URL patterns. This helps in namespacing the URLs when including them elsewhere.
app_name = 'agents'

# Defining the URL patterns for the application.
urlpatterns = [
    # Mapping the URL "landing" to the index view in the views module. The name "landing" is used for URL reversing.
    path("landing", views.index, name="landing")
]
