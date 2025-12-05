from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from app.core.views import CustomPageNumberPagination
from app.global_constants import SuccessMessage, ErrorMessage
from app.rss.models import RSSFeed
from app.rss.serializers import RSSFeedCreateSerializer, RSSFeedDisplaySerializer, RSSFeedUpdateSerializer, \
    RSSFeedListFilterDisplaySerializer
from app.utils import get_response_schema
from permissions import IsSuperAdmin


# Create your views here.
class RSSFeedCreateApiView(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSuperAdmin]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING, description='Title'),
                'url': openapi.Schema(type=openapi.TYPE_STRING, description='URL'),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='Description'),
            }
        )
    )
    def post(self, request):
        serializer = RSSFeedCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return get_response_schema(serializer.data, SuccessMessage.RECORD_CREATED.value,
                                       status.HTTP_201_CREATED, )
        return get_response_schema(serializer.errors, ErrorMessage.BAD_REQUEST.value, status.HTTP_400_BAD_REQUEST)


class RSSFeedDetailApiView(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSuperAdmin]

    def get_object(self, pk):

        rss_feed_queryset = RSSFeed.objects.filter(pk=pk, is_active=True)
        if rss_feed_queryset.exists():
            return rss_feed_queryset.first()
        return None

    def get(self, request, pk):

        rss_feed = self.get_object(pk)
        if rss_feed is None:
            return get_response_schema(None, ErrorMessage.NOT_FOUND.value, status.HTTP_404_NOT_FOUND)
        serializer = RSSFeedDisplaySerializer(rss_feed)
        return get_response_schema(serializer.data, SuccessMessage.RECORD_RETRIEVED.value,
                                   status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING, description='Title'),
                'url': openapi.Schema(type=openapi.TYPE_STRING, description='URL'),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='Description'),
            }
        )
    )
    def put(self, request, pk):
        rss_feed = self.get_object(pk)
        if rss_feed is None:
            return get_response_schema(None, ErrorMessage.NOT_FOUND.value, status.HTTP_404_NOT_FOUND)
        serializer = RSSFeedUpdateSerializer(rss_feed, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return get_response_schema(serializer.data, SuccessMessage.RECORD_UPDATED.value,
                                       status.HTTP_200_OK)
        return get_response_schema(serializer.errors, ErrorMessage.BAD_REQUEST.value, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        rss_feed = self.get_object(pk)
        if rss_feed is None:
            return get_response_schema(None, ErrorMessage.NOT_FOUND.value, status.HTTP_404_NOT_FOUND)
        rss_feed.is_active = False
        rss_feed.save()
        return get_response_schema(None, SuccessMessage.RECORD_DELETED.value, status.HTTP_204_NO_CONTENT)


class RSSFeedListFilterApiView(ListAPIView):
    serializer_class = RSSFeedListFilterDisplaySerializer
    pagination_class = CustomPageNumberPagination

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSuperAdmin]

    def get_queryset(self):

        query_params = self.request.query_params

        rss_feed_queryset = RSSFeed.objects.filter(is_active=True).order_by('-updated')

        if query_params.get('title'):
            rss_feed_queryset = rss_feed_queryset.filter(title__istartswith=query_params.get('title'))
        if query_params.get('url'):
            rss_feed_queryset = rss_feed_queryset.filter(url__istartswith=query_params.get('url'))

        return rss_feed_queryset

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('title', openapi.IN_QUERY, description='Title', type=openapi.TYPE_STRING),
            openapi.Parameter('url', openapi.IN_QUERY, description='URL', type=openapi.TYPE_STRING),
        ]
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
