from django.urls import path

from app.rss.views import RSSFeedCreateApiView, RSSFeedDetailApiView, RSSFeedListFilterApiView

urlpatterns = [
    # Authentication
    path('', RSSFeedCreateApiView.as_view(), name='rss-feed-create'),
    path('<int:pk>', RSSFeedDetailApiView.as_view(), name='rss-feed-detail'),
    path('list-filter', RSSFeedListFilterApiView.as_view(), name='rss-feed-list-filter'),
]
