from django.urls import include, path
from institution.views import (
    InstitutionListView,
    InstitutionRegistrationView,
    InstitutionProfileView,
    InstitutionEditBasicView,
    InstitutionEditAddressView,
    InstitutionDetailView,
    LegalRepresentativeEditView,
    DomainVerificationRequestView
)


urlpatterns = [
    path('list/', InstitutionListView.as_view(), name='institution_list'),
    path('registration/', InstitutionRegistrationView.as_view(), name='institution_registration'),
    path('profile/', InstitutionProfileView.as_view(), name='institution_profile'),
    path('edit/', include([
        path('basic/', InstitutionEditBasicView.as_view(), name='institution_edit_basic'),
        path('address/', InstitutionEditAddressView.as_view(), name='institution_edit_address')
    ])),
    path('detail/<int:institution_id>/', InstitutionDetailView.as_view(), name='institution_detail'),
    path('representative/', include([
        path('edit/', LegalRepresentativeEditView.as_view(), name='legal_representative_edit')
    ])),
    path('domain-verification/', include([
        path('request/', DomainVerificationRequestView.as_view(), name='domain_verification_request')
    ])),
]
