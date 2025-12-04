from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.
class Goal(models.Model):
    # Foreign Key
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='user_goals',
                             related_query_name='user_goal', unique=True)

    # Field declarations
    topic = models.CharField(max_length=255)
    duration = models.IntegerField(default=7)

    # Additional fields
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
