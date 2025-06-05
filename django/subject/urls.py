from django.urls import path
from subject.views import (
    # SubjectListView,
    SubjectRegistrationView,
    SubjectProfileView,
    SubjectEditView
)

urlpatterns = [
    # path('list/', SubjectListView.as_view(), name='subject_list'),
    path('registration/', SubjectRegistrationView.as_view(), name='subject_registration'),
    path('profile/', SubjectProfileView.as_view(), name='subject_profile'),
    path('edit/', SubjectEditView.as_view(), name='subject_edit'),
]
