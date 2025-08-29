from django.urls import path
from document.views import (
    DocumentListView,
    DocumentUploadView,
    DocumentDetailView
)


urlpatterns = [
    path('list/', DocumentListView.as_view(), name='document_list'),
    path('upload/', DocumentUploadView.as_view(), name='document_upload'),
    path('detail/<int:document_id>/', DocumentDetailView.as_view(), name='document_detail')
]
