from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from django.urls import reverse


class SubjectRequiredMixin(AccessMixin):
    """Verify that the current user is a subject and is authenticated."""

    def get_redirect_url(self):
        return reverse('home')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if not request.user.is_subject:
            messages.error(
                request,
                'Você não tem permissão para acessar esta página. '
                'Desculpe, este recurso só está disponível para instituições.'
            )
            return redirect(reverse('home'))

        return super().dispatch(request, *args, **kwargs)
