from django.db import models

# Create your models here.
class RSSFeed(models.Model):

    #Field details
    title = models.CharField(max_length=255)
    url = models.URLField()
    description = models.TextField(blank=True,null=True)

    #additional fields
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

