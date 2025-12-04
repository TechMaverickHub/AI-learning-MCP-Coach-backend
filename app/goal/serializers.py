from rest_framework import serializers

from app.goal.models import Goal


class GoalCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ('topic', 'duration', 'user')


class GoalDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ('topic', 'duration')

class GoalUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ('topic', 'duration')
