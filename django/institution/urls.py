from django.urls import path
from institution.views import (
    InstitutionRegistrationView
)

urlpatterns = [
    path('registration/', InstitutionRegistrationView.as_view(), name='institution_registration')
]
