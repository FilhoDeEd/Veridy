from django.urls import include, path
from institution.views import (
    InstitutionListView,
    InstitutionRegistrationView,
    InstitutionProfileView,
    InstitutionEditBasicView,
    InstitutionEditAddressView,
    InstitutionDetailView,
    InstitutionVerificationRequestTokenView,
    InstitutionVerificationDisplayTokenView,
    InstitutionVerificationDownloadTokenView,
    InstitutionVerificationCheckTokenView,
    LegalRepresentativeEditView
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
    path('verification/', include([
        path('request-token/', InstitutionVerificationRequestTokenView.as_view(), name='verification_request_token'),
        path('display-token/', InstitutionVerificationDisplayTokenView.as_view(), name='verification_display_token'),
        path('download-token/', InstitutionVerificationDownloadTokenView.as_view(), name='verification_download_token'),
        path('check-token/', InstitutionVerificationCheckTokenView.as_view(), name='verification_check_token')
    ]))
]
