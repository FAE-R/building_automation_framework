from django.urls import path
from . import views
from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'metric', views.MetricViewSet, basename='Metric')
router.register(r'metadata', views.MetadataViewSet, basename='Metadata')
router.register(r'userprofile', views.UserProfile, basename='Profile')
router.register(r'roomprofile', views.RoomProfile, basename='Room')
router.register(r'tracker', views.MetricTrackerViewSet, basename='Tracker')
router.register(r'roomusers', views.RoomUserViewSet, basename='RoomUsers')
router.register(r'feedback', views.ComfortFeedbackViewSet, basename='Feedback')
router.register(r'building', views.BuildingViewSet, basename='Building')
router.register(r'schedualer', views.SchedulerViewSet, basename='Schedualer')
router.register(r'monitoring', views.RoomMonitoringViewSet,
                basename='Monitoring')
router.register(r'plot', views.RoomMonitoringDataViewSet,
                basename='Plot')
router.register(r'notification', views.NotificationViewSet,
                basename='Notification')
router.register(r'taskresult', views.TaskResultViewSet,
                basename='Taskresult')
router.register(r'weekschedule', views.WeekScheduleViewSet,
                basename='Weekschedule')


app_name = 'rest_api'

urlpatterns = [
    path("landing", views.index, name="landing"),
    path('', include(router.urls)),
    path('token/auth/', views.CustomAuthToken.as_view()),
]
