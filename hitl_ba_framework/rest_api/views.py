from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions, authentication
from .serializers import MetricSerializer, MetadataSerializer, ProfileSerializer, RoomSerializer, RoomUserSerializer, ComfortFeedbackSerializer, BuildingSerializer, SchedulerSerializer, RoomMonitoringSerializer, TaskResultSerializer
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
from agents.models import Profile, Room, Room_Users, Room_Monitoring_Datapoints, Comfort_Feedback, Building, Scheduler, Notification
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


class RoomProfile(viewsets.ModelViewSet):
    """
    API endpoint for handling user profile data
    """
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = RoomSerializer

    def get_queryset(self):
        """
        Return room data
        """
        user_id = Token.objects.get(key=self.request.auth).user_id
        user = User.objects.get(id=user_id)
        profile = Profile.objects.get(user=user)
        room_id = self.request.query_params.get('room')
        if Room.objects.filter(name=room_id).exists():
            room_q = Room.objects.get(name=room_id)
            if Room_Users.objects.filter(user__pk=user_id, room__name=room_q.name).exists():
                return Room.objects.filter(name=room_q.name)

    @action(detail=True, methods=['put'])
    def set_control_mode(self, request, pk=None):
        """
        Changing room control mode
        """
        user_id = Token.objects.get(key=self.request.auth).user_id
        user = User.objects.get(id=user_id)
        profile = Profile.objects.get(user=user)
        room_id = self.request.query_params.get('room')
        if Room.objects.filter(name=room_id).exists():
            room_q = Room.objects.get(name=room_id)
            if Room_Users.objects.filter(user=profile, room=room_q).exists():
                serializer = RoomSerializer().update(room_q, self.request.data, profile)
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


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


class RoomUserViewSet(viewsets.ModelViewSet):
    serializer_class = RoomUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get_queryset(self):
        user_id = Token.objects.get(key=self.request.auth).user_id
        user = User.objects.get(id=user_id)
        return Room_Users.objects.filter(user__user=user, still_use_room=True)

    @action(detail=True, methods=['get'])
    def rooms_list(self, request, pk=None):
        """
        Get user room list
        """
        user_id = Token.objects.get(key=self.request.auth).user_id
        user = User.objects.get(id=user_id)
        room_list_ids = Room_Users.objects.filter(
            user__user=user, still_use_room=True)
        room_list = {}
        for i in room_list_ids:
            room_list["room_"+str(i.room.id)] = i.room.name
        return Response(room_list)


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = RoomUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    @action(detail=True, methods=['get'])
    def last_notification(self, request, pk=None):
        """
        Get last notification
        """
        user_id = Token.objects.get(key=self.request.auth).user_id
        user = User.objects.get(id=user_id)
        rooms = Room_Users.objects.filter(user__pk=user_id).values_list('room')

        try:
            last_notification = Notification.objects.filter(user=Profile.objects.get(user=user),
                room__in=rooms).last()

            return Response({"title": last_notification.title, "message": last_notification.message})
        except:
            return Response({"title": "Hello", "message": "You do not have any notification."})


class ComfortFeedbackViewSet(viewsets.ModelViewSet):
    serializer_class = ComfortFeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get_queryset(self):
        user_id = Token.objects.get(key=self.request.auth).user_id
        user = User.objects.get(id=user_id)
        room_id = self.request.query_params.get('room')
        if user.is_superuser:
            return Comfort_Feedback.objects.filter(room__name=room_id).exclude(user=Profile.objects.get(pk=1))
        profile = Profile.objects.get(user=user)
        if Room.objects.filter(name=room_id).exists():
            room_q = Room.objects.get(name=room_id)
            if Room_Users.objects.filter(user=profile, room=room_q, still_use_room=True).exists():
                return Comfort_Feedback.objects.filter(user__pk=user_id, room__name=room_q.name)

    @action(detail=True, methods=['post'])
    def send_feedback(self, request, pk=None):
        """
        Send user feedback about thermal comfort
        """
        user_id = Token.objects.get(key=self.request.auth).user_id
        user = User.objects.get(id=user_id)
        room_id = self.request.query_params.get('room')
        profile = Profile.objects.get(user=user)
        if Room.objects.filter(name=room_id).exists():
            room_q = Room.objects.get(name=room_id)
            if Room_Users.objects.filter(user=profile, room=room_q, still_use_room=True).exists():
                table_list = Room_Monitoring_Datapoints.objects.get(
                    room=room_q)
                feedback = Comfort_Feedback(room=room_q, user=profile)
                feedback.feedback = int(self.request.data.get("feedback"))
                if table_list is not None:
                    ranges = (timezone.now() -
                              timedelta(hours=1), timezone.now())
                    # ranges_door = (timezone.now() -
                    #                timedelta(days=1), timezone.now())
                    if table_list.temperature != None:
                        table = apps.get_model(
                            'logger', table_list.temperature)
                        value = table.timescale.filter(
                            time__range=ranges).last()
                        if value != None:
                            feedback.temperature = value.value

                    if table_list.temperature_out != None:
                        table = apps.get_model(
                            'logger', table_list.temperature_out)
                        value = table.timescale.filter(
                            time__range=ranges).last()
                        if value != None:
                            feedback.temperature_out = value.value

                    if table_list.humidity != None:
                        table = apps.get_model(
                            'logger', table_list.humidity)
                        value = table.timescale.filter(
                            time__range=ranges).last()
                        if value != None:
                            feedback.humidity = value.value

                    if table_list.co2 != None:
                        table = apps.get_model(
                            'logger', table_list.co2)
                        value = table.timescale.filter(
                            time__range=ranges).last()
                        if value != None:
                            feedback.co2 = value.value


                    if table_list.light != None:
                        table = apps.get_model(
                            'logger', table_list.light)
                        value = table.timescale.filter(
                            time__range=ranges).last()
                        if value != None:
                            feedback.light = value.value

                    # status_d = -1
                    # if table_list.doors_open != None:
                    #     table_lists = table_list.doors_open.split(",")
                    #     for table in table_lists:
                    #         table = apps.get_model(
                    #             'logger', table)
                    #         value = table.timescale.filter(
                    #             time__range=ranges_door).last()
                    #         if value != None:
                    #             if value.value == 0:
                    #                 if status_d != 1:
                    #                     status_d = 0
                    #             elif value.value == 1:
                    #                 status_d = 1

                    #     feedback.door_open = status_d

                    # status_w = -1
                    # if table_list.windows_open != None:
                    #     table_lists = table_list.windows_open.split(",")
                    #     for table in table_lists:
                    #         table = apps.get_model(
                    #             'logger', table)
                    #         value = table.timescale.filter(
                    #             time__range=ranges_door).last()
                    #         if value != None:
                    #             if value.value == 0:
                    #                 if status_w != 1:
                    #                     status_w = 0
                    #             elif value.value == 1:
                    #                 status_w = 1
                    #     feedback.windows_open = status_w
                            
                    feedback.datetime = timezone.now()

                    feedback.save()

                    return Response(status=status.HTTP_200_OK)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class MetricTrackerViewSet(viewsets.ModelViewSet):
    serializer_class = MetadataSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get_queryset(self):
        user_id = Token.objects.get(key=self.request.auth).user_id
        user = User.objects.get(id=user_id)
        room_id = self.request.query_params.get('room')
        if Room.objects.filter(name=room_id).exists():
            room_q = Room.objects.get(name=room_id)
            if Room_Users.objects.filter(user__pk=user_id, room__name=room_q.name).exists():
                table_id = Room_Users.objects.filter(
                    user__pk=user_id, room__name=room_q.name).tracker_table
                table = apps.get_model('logger', table_id)
                ranges = (timezone.now() - timedelta(days=7), timezone.now())
                return table.timescale.filter(time__range=ranges).last()

    @action(detail=True, methods=['put'])
    def set_tracker(self, request, pk=None):
        """
        Changing room control mode
        """
        user_id = Token.objects.get(key=self.request.auth).user_id
        user = User.objects.get(id=user_id)
        room_id = self.request.query_params.get('room')
        if Room.objects.filter(name=room_id).exists():
            room_q = Room.objects.get(name=room_id)
            if Room_Users.objects.filter(user__pk=user_id, room__name=room_q.name).exists():
                table_id = Room_Users.objects.get(
                    user__pk=user_id, room__name=room_q.name).tracker_table

                Metric = apps.get_model('logger', table_id)
                metric = Metric()
                metric.value = float(self.request.data.get("value"))
                metric.time = datetime.fromtimestamp(int(float(self.request.data.get("timestamp")))/1000).astimezone(
                    pytz.timezone(timezone.get_current_timezone_name()))
                metric.save()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


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


class MetadataViewSet(viewsets.ModelViewSet):
    serializer_class = MetadataSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get_queryset(self):
        model_name = self.request.query_params.get('datapoint')
        if model_name != "all":
            return MetaData.objects.all().filter(table_id=model_name)
        else:
            return MetaData.objects.all()


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

class SchedulerViewSet(viewsets.ModelViewSet):
    """
    API endpoint for handling user profile data
    """
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = SchedulerSerializer

    @action(detail=True, methods=['get'])
    def get_room_accupancy(self, request, pk=None):
        """
        Return room scheduler data
        """
        user_id = Token.objects.get(key=self.request.auth).user_id
        user = User.objects.get(id=user_id)
        profile = Profile.objects.get(user=user)
        room_id = self.request.query_params.get('room')
        if Room.objects.filter(name=room_id).exists():
            room_q = Room.objects.get(name=room_id)
            if Room_Users.objects.filter(user__pk=user_id, room__name=room_q.name).exists():
                # return Scheduler.objects.filter(room=room_q)
                return Response({"room": room_id, "weekly_room_accupancy": [80, 50, 10, 50, 60, 0, 0]})
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class WeekScheduleViewSet(viewsets.ModelViewSet):
    """
    API endpoint
    """
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = SchedulerSerializer

    def get_queryset(self):
        """
        Return room scheduler data
        """
        user_id = Token.objects.get(key=self.request.auth).user_id
        user = User.objects.get(id=user_id)
        profile = Profile.objects.get(user=user)
        room_id = self.request.query_params.get('room')
        if Room.objects.filter(name=room_id).exists():
            room_q = Room.objects.get(name=room_id)
            return Scheduler.objects.filter(room=room_q).order_by("-day_of_week", "-hour", "-quarter")
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class RoomMonitoringViewSet(viewsets.ModelViewSet):
    """
    API endpoint for handling room monitoring data
    """
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = RoomMonitoringSerializer

    @action(detail=True, methods=['get'])
    def get_current_data(self, request, pk=None):
        user_id = Token.objects.get(key=self.request.auth).user_id
        user = User.objects.get(id=user_id)
        profile = Profile.objects.get(user=user)
        room_id = self.request.query_params.get('room')
        if Room.objects.filter(name=room_id).exists():
            room_q = Room.objects.get(name=room_id)
            if Room_Users.objects.filter(user=profile, room=room_q).exists():
                table_list = Room_Monitoring_Datapoints.objects.get(
                    room=room_q)
                if table_list is not None:
                    data = {}
                    ranges = (timezone.now() -
                              timedelta(hours=1), timezone.now())
                    ranges_door = (timezone.now() -
                                   timedelta(days=1), timezone.now())
                    if table_list.temperature != None:
                        table = apps.get_model(
                            'logger', table_list.temperature)
                        value = table.timescale.filter(
                            time__range=ranges).last()
                        if value != None:
                            data["temperature"] = value.value
                        else:
                            data["temperature"] = 99
                    if table_list.humidity != None:
                        table = apps.get_model(
                            'logger', table_list.humidity)
                        value = table.timescale.filter(
                            time__range=ranges).last()
                        if value != None:
                            data["humidity"] = value.value
                        else:
                            data["humidity"] = -99
                    if table_list.co2 != None:
                        table = apps.get_model(
                            'logger', table_list.co2)
                        value = table.timescale.filter(
                            time__range=ranges).last()
                        if value != None:
                            data["co2"] = value.value
                        else:
                            data["co2"] = -99

                    if table_list.light != None:
                        table = apps.get_model(
                            'logger', table_list.light)
                        value = table.timescale.filter(
                            time__range=ranges).last()
                        if value != None:
                            data["light"] = value.value
                        else:
                            data["light"] = -99
                    if table_list.doors_open != None:
                        table_lists = table_list.doors_open.split(",")
                        status = "invalid"
                        for table in table_lists:
                            table = apps.get_model(
                                'logger', table)
                            value = table.timescale.filter(
                                time__range=ranges_door).last()
                            if value != None:
                                if value.value == 0:
                                    if status != "open":
                                        status = "closed"
                                elif value.value == 1:
                                    status = "open"
                        data["doors_open"] = status
                    if table_list.windows_open != None:
                        table_lists = table_list.windows_open.split(",")
                        status = "invalid"
                        for table in table_lists:
                            table = apps.get_model(
                                'logger', table)
                            value = table.timescale.filter(
                                time__range=ranges_door).last()
                            if value != None:
                                if value.value == 0:
                                    if status != "open":
                                        status = "closed"
                                elif value.value == 1:
                                    status = "open"
                        data["windows_open"] = status

                    return Response(data)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class RoomMonitoringDataViewSet(viewsets.ModelViewSet):
    """
    API endpoint for handling room monitoring data
    """
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = RoomMonitoringSerializer

    @action(detail=True, methods=['get'])
    def get_current_data(self, request, pk=None):
        user_id = Token.objects.get(key=self.request.auth).user_id
        user = User.objects.get(id=user_id)
        profile = Profile.objects.get(user=user)
        room_id = self.request.query_params.get('room')
        if Room.objects.filter(name=room_id).exists():
            room_q = Room.objects.get(name=room_id)
            if Room_Users.objects.filter(user=profile, room=room_q).exists():
                table_list = Room_Monitoring_Datapoints.objects.get(
                    room=room_q)
                if table_list is not None:
                    data = {}
                    ranges = (timezone.now() -
                              timedelta(hours=3), timezone.now())
                    ranges_weather = (timezone.now() -
                                      timedelta(minutes=30), timezone.now() + timedelta(minutes=30))
                    ranges_door = (timezone.now() -
                                   timedelta(days=1), timezone.now())
                    if table_list.temperature != None:
                        table = apps.get_model(
                            'logger', table_list.temperature)
                        value = table.timescale.filter(
                            time__range=ranges)
                        if value != None:
                            data["temperature"] = value.values_list(
                                "value", "time")
                        else:
                            data["temperature"] = []
                    if table_list.temperature_out != None:
                        table = apps.get_model(
                            'logger', table_list.temperature_out)
                        value = table.timescale.filter(
                            time__range=ranges_weather)
                        if value != None:
                            data["outdoor_temperature"] = value.values_list(
                                "value", "time")
                        else:
                            data["outdoor_temperature"] = []
                    if table_list.humidity != None:
                        table = apps.get_model(
                            'logger', table_list.humidity)
                        value = table.timescale.filter(
                            time__range=ranges)
                        if value != None:
                            data["humidity"] = value.values_list(
                                "value", "time")
                        else:
                            data["humidity"] = []
                    if table_list.co2 != None:
                        table = apps.get_model(
                            'logger', table_list.co2)
                        value = table.timescale.filter(
                            time__range=ranges)
                        if value != None:
                            data["co2"] = value.values_list(
                                "value", "time")
                        else:
                            data["co2"] = []

                    if table_list.doors_open != None:
                        table_lists = table_list.doors_open.split(",")
                        for table in table_lists:
                            table = apps.get_model(
                                'logger', table)
                            value = table.timescale.filter(
                                time__range=ranges_door)
                            if value != None:
                                data["door_status"] = value.values_list(
                                    "value", "time")
                            else:
                                data["door_status"] = []
                    if table_list.windows_open != None:
                        table_lists = table_list.windows_open.split(",")
                        data["windows_status"] = []
                        for table in table_lists:
                            table = apps.get_model(
                                'logger', table)
                            value = table.timescale.filter(
                                time__range=ranges_door)
                            if value != None:
                                data["windows_status"].append(value.values_list(
                                    "value", "time"))

                    return Response(data)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
