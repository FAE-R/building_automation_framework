from django.urls import path
from . import views
from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'metric', views.MetricViewSet, basename='Metric')
router.register(r'building', views.BuildingViewSet, basename='Building')
router.register(r'taskresult', views.TaskResultViewSet,
                basename='Taskresult')


app_name = 'rest_api'

urlpatterns = [
    path("landing", views.index, name="landing"),
    path('', include(router.urls)),
    path('token/auth/', views.CustomAuthToken.as_view()),
]
