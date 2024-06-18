from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions, authentication
from .serializers import MetricSerializer, MetadataSerializer
from logger.models import *
from django.apps import apps
from django.utils import timezone
from datetime import timedelta
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from datetime import datetime
from agents.tasks import my_new_task


def index(request):
    return render(request, "agents/index.html")



#
