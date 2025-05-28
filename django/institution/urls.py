from django.urls import include, path
from institution.views import (
    InstitutionProfileView,
    InstitutionListView,
    InstitutionRegistrationView,
    InstitutionEditView,
    LegalRepresentativeEditView
)


urlpatterns = [
    path('', InstitutionProfileView.as_view(), name='institution_profile'),
    path('list/', InstitutionListView.as_view(), name='institution_list'),
    path('registration/', InstitutionRegistrationView.as_view(), name='institution_registration'),
    path('edit/', InstitutionEditView.as_view(), name='institution_edit'),
    path('representative/', include([
        path('edit/', LegalRepresentativeEditView.as_view(), name='legal_representative_edit')
    ]))
]
