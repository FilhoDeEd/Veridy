from django.urls import path
from institution.views import (
    InstitutionProfileView,
    InstitutionRegistrationView,
    InstitutionEditView
)


urlpatterns = [
    path('', InstitutionProfileView.as_view(), name='institution_profile'),
    path('registration/', InstitutionRegistrationView.as_view(), name='institution_registration'),
    path('edit/', InstitutionEditView.as_view(), name='institution_edit')
]
