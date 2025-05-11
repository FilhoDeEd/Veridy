from django.urls import path
from institution.views import (
    InstitutionProfileView,
    InstitutionRegistrationView
)


urlpatterns = [
    path('', InstitutionProfileView.as_view(), name='institution_profile'),
    path('registration/', InstitutionRegistrationView.as_view(), name='institution_registration')
]
