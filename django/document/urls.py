from django.urls import path
from document.views import (
    DocumentListView,
    DocumentUploadView
)


urlpatterns = [
    path('list/', DocumentListView.as_view(), name='document_list'),
    path('upload/', DocumentUploadView.as_view(), name='document_upload')
]
