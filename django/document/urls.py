from django.urls import include, path
from document.views import (
    DocumentUploadView
)


urlpatterns = [
    path('upload/', DocumentUploadView.as_view(), name='document_upload'),
]
