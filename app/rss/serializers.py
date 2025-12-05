from rest_framework import serializers

from app.rss.models import RSSFeed


class RSSFeedCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RSSFeed
        fields = ['title', 'url', 'description']


class RSSFeedUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RSSFeed
        fields = ['title', 'url', 'description']


class RSSFeedDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = RSSFeed
        fields = ['title', 'url', 'description']


class RSSFeedListFilterDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = RSSFeed
        fields = ['title', 'url', 'description']
