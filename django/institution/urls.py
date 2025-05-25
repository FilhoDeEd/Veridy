from django.urls import include, path
from institution.views import (
    InstitutionProfileView,
    InstitutionRegistrationView,
    InstitutionEditView,
    LegalRepresentativeEditView
)


urlpatterns = [
    path('', InstitutionProfileView.as_view(), name='institution_profile'),
    path('registration/', InstitutionRegistrationView.as_view(), name='institution_registration'),
    path('edit/', InstitutionEditView.as_view(), name='institution_edit'),
    path('representative/', include([
        path('edit/', LegalRepresentativeEditView.as_view(), name='legal_representative_edit')
    ]))
]
