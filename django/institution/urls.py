from django.urls import include, path
from institution.views import (
    InstitutionListView,
    InstitutionRegistrationView,
    InstitutionProfileView,
    InstitutionEditView,
    LegalRepresentativeEditView
)


urlpatterns = [
    path('list', InstitutionListView.as_view(), name='institution_list'),
    path('registration/', InstitutionRegistrationView.as_view(), name='institution_registration'),
    path('profile/', InstitutionProfileView.as_view(), name='institution_profile'),
    path('edit/', InstitutionEditView.as_view(), name='institution_edit'),
    path('representative/', include([
        path('edit/', LegalRepresentativeEditView.as_view(), name='legal_representative_edit')
    ]))
]
