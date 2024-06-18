from django.urls import path
from . import views

app_name = 'logger'
urlpatterns = [
    path('', views.home, name='home')
]