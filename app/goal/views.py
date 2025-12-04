from django.db import transaction
from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from app.global_constants import SuccessMessage, ErrorMessage
from app.goal.models import Goal
from app.goal.rag_pipeline import generate_learning_suggestions
from app.goal.serializers import GoalCreateSerializer, GoalDisplaySerializer, GoalUpdateSerializer
from app.utils import get_response_schema
from permissions import IsUser


# Create your views here.
class GoalCreateApiView(GenericAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsUser]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'topic': openapi.Schema(type=openapi.TYPE_STRING, description="topic"),
                'duration': openapi.Schema(type=openapi.TYPE_INTEGER, description="duration"),

            }
        )
    )
    def post(self, request):
        with transaction.atomic():

            request.data['user'] = self.request.user.id
            serializer = GoalCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()

                return get_response_schema(serializer.data, SuccessMessage.RECORD_CREATED.value,
                                           status.HTTP_201_CREATED, )

            return get_response_schema(serializer.errors, ErrorMessage.BAD_REQUEST.value, status.HTTP_400_BAD_REQUEST)


class GoalDetailApiView(GenericAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsUser]

    def get_object(self, pk):

        goal_queryset = Goal.objects.filter(pk=pk, is_active=True, user_id=self.request.user.id)

        if goal_queryset.exists():
            return goal_queryset.first()

        return None

    def get(self, request, pk):

        goal = self.get_object(pk)

        if not goal:
            return get_response_schema(None, ErrorMessage.NOT_FOUND.value, status.HTTP_404_NOT_FOUND)

        serializer = GoalDisplaySerializer(goal)

        return get_response_schema(serializer.data, SuccessMessage.RECORD_RETRIEVED.value, status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'topic': openapi.Schema(type=openapi.TYPE_STRING, description="topic"),
                'duration': openapi.Schema(type=openapi.TYPE_INTEGER, description="duration"),

            }
        )
    )
    def put(self, request, pk):

        goal = self.get_object(pk)

        if not goal:
            return get_response_schema(None, ErrorMessage.NOT_FOUND.value, status.HTTP_404_NOT_FOUND)

        serializer = GoalUpdateSerializer(goal, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return get_response_schema(serializer.data, SuccessMessage.RECORD_UPDATED.value, status.HTTP_200_OK)

        return get_response_schema(serializer.errors, ErrorMessage.BAD_REQUEST.value, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):

        goal = self.get_object(pk)

        if not goal:
            return get_response_schema(None, ErrorMessage.NOT_FOUND.value, status.HTTP_404_NOT_FOUND)

        goal.is_active = False
        goal.save()

        return get_response_schema(None, SuccessMessage.RECORD_DELETED.value, status.HTTP_204_NO_CONTENT)


class GoalGeneratePlanApiView(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsUser]

    def get_object(self, pk):
        goal_queryset = Goal.objects.filter(pk=pk, is_active=True, user_id=self.request.user.id)

        if goal_queryset.exists():
            return goal_queryset.first()

        return None

    def post(self, request, pk):
        goal = self.get_object(pk)

        if not goal:
            return get_response_schema(None, ErrorMessage.NOT_FOUND.value, status.HTTP_404_NOT_FOUND)

        plan = generate_learning_suggestions(goal.topic, goal.duration)

        return_data = {"goal": goal.topic, "plan": plan, "duration": goal.duration}

        return get_response_schema(return_data, SuccessMessage.RECORD_RETRIEVED.value, status.HTTP_200_OK)
