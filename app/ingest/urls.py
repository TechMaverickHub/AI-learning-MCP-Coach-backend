from django.urls import path

from app.ingest.views import DocumentIngestApiView

urlpatterns = [
    # Authentication
    path('', DocumentIngestApiView.as_view(), name='document-ingest'),

]
