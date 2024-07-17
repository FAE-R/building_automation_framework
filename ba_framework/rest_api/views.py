from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions, authentication
from .serializers import MetricSerializer, ProfileSerializer, RoomSerializer, BuildingSerializer, TaskResultSerializer
from logger.models import *
from django.apps import apps
from django.utils import timezone
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from datetime import datetime
from django.contrib.auth.models import User
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.decorators import action
from agents.models import Profile, Room, Building
from django_celery_results.models import TaskResult
from datetime import timedelta
import pytz


def index(request):
    return render(request, "rest_api/index.html")


class BuildingViewSet(viewsets.ModelViewSet):
    """
    API endpoint for handling building
    """
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = BuildingSerializer

    def get_queryset(self):
        """
        Return building data
        """
        user_id = Token.objects.get(key=self.request.auth).user_id
        user = User.objects.get(id=user_id)
        profile = Profile.objects.get(user=user)
        return Building.objects.filter(id=profile.building.id)


class UserProfile(viewsets.ModelViewSet):
    """
    API endpoint for handling user profile data
    """
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = ProfileSerializer

    def get_queryset(self):
        """
        Return user profile data
        """
        user_id = Token.objects.get(key=self.request.auth).user_id
        user = User.objects.get(id=user_id)
        profile = Profile.objects.filter(user=user)
        return profile

    @action(detail=True, methods=['put'])
    def set_profile(self, request, pk=None):
        """
        Changing user profile data
        """
        user_id = Token.objects.get(key=self.request.auth).user_id
        user = User.objects.get(id=user_id)
        profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer().update(profile, self.request.data)
        return Response(status=status.HTTP_200_OK)




class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


class MetricViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows metric to be viewed.
    """
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get_queryset(self):

        model_name = self.request.query_params.get('datapoint')
        table_i = apps.get_model('logger', model_name)
        request_time_from = self.request.query_params.get('from')
        request_time_to = self.request.query_params.get('to')

        if request_time_to == "now":
            datetime_to = timezone.now()
        else:
            datetime_to = datetime.strptime(
                request_time_to, '%Y-%m-%dT%H:%M:%S')

        datetime_from = datetime.strptime(
            request_time_from, '%Y-%m-%dT%H:%M:%S')

        ranges = (datetime_from, datetime_to)
        queryset = table_i.timescale.filter(time__range=ranges)

        return queryset

    def get_serializer_class(self):
        model_name = self.request.query_params.get('datapoint')
        data = MetricSerializer
        MetricSerializer.Meta.model = apps.get_model('logger', model_name)
        return data


class TaskResultViewSet(viewsets.ModelViewSet):
    serializer_class = TaskResultSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get_queryset(self):
        task_name = self.request.query_params.get('task_name')
        if task_name is not None:
            request_time_from = self.request.query_params.get('from')
            request_time_to = self.request.query_params.get('to')

            if request_time_to == "now":
                datetime_to = timezone.now()
            else:
                datetime_to = datetime.strptime(
                    request_time_to, '%Y-%m-%dT%H:%M:%S').astimezone(pytz.utc)

            datetime_from = datetime.strptime(
                request_time_from, '%Y-%m-%dT%H:%M:%S').astimezone(pytz.utc)

            ranges = (datetime_from, datetime_to)
            return TaskResult.objects.filter(periodic_task_name=task_name, date_done__range=ranges)
        else:
            return TaskResult.objects.all()[:10]

