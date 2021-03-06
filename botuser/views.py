import os
import datetime
from chatbot import settings
from slack import WebClient
from slack.errors import SlackApiError
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status, generics, mixins
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response

from .serializers import Send_Message_Serializer, Schedule_Message_Serializer, Join_Conversation_Serializer
from .models import Send_Message, Schedule_Message, Conversation
from django_slack_oauth.models import SlackOAuthRequest


class Send_Message_View(generics.GenericAPIView,
                        mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.RetrieveModelMixin,):

    serializer_class = Send_Message_Serializer
    queryset = Send_Message.objects.all()
    lookup_field = 'id'

    def get(self, request, id=None):
        '''
        GET Request
        '''
        if id:
            return self.retrieve(request, id)
        else:
            return self.list(request)

    @csrf_exempt
    def post(self, request):
        '''
        Create Request
        '''
        return self.create(request)


class Schedule_Message_View(generics.GenericAPIView,
                            mixins.CreateModelMixin,
                            mixins.ListModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin,
                            mixins.RetrieveModelMixin,):

    serializer_class = Schedule_Message_Serializer
    queryset = Schedule_Message.objects.all()
    lookup_field = 'id'

    def get(self, request, id=None):
        '''
        GET Request
        '''

        if id:
            return self.retrieve(request, id)
        else:
            return self.list(request)

    @csrf_exempt
    def post(self, request):
        '''
        Create Request
        '''
        return self.create(request)
class List_Conversation_View(APIView):
    token = str(SlackOAuthRequest.objects.last())
    def get(self, request):
        client = WebClient(
                    token=self.token)
        try:
            response = client.conversations_list()
            conversations = response["channels"]
            return Response(conversations)
        except SlackApiError as e:
            assert e.response["ok"] is False
            assert e.response["error"]
            return Response(f"Got an error: {e.response}", status=status.HTTP_400_BAD_REQUEST)

class Join_Conversation_View(generics.GenericAPIView,
                            mixins.CreateModelMixin,
                            mixins.ListModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin,
                            mixins.RetrieveModelMixin,):

    serializer_class = Join_Conversation_Serializer
    queryset = Conversation.objects.all()
    lookup_field = 'id'

    def get(self, request, id=None):
        '''
        GET Request
        '''

        if id:
            return self.retrieve(request, id)
        else:
            return self.list(request)
    @csrf_exempt
    def post(self, request):
        token = str(SlackOAuthRequest.objects.last())
        serializer = self.serializer_class(data=request.data)
        client = WebClient(
                    token=token)
        if serializer.is_valid():
            try:
                response = client.conversations_join(
                            channel=serializer.validated_data.get('conversation_id'),
                        )
                serializer.save()
                return Response("Joined the Channel")
            except SlackApiError as e:
                assert e.response["ok"] is False
                assert e.response["error"]
                return Response(f"Got an error: {e.response}", status=status.HTTP_400_BAD_REQUEST)