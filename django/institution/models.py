from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


UserModel = get_user_model()


class LegalRepresentative(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    role = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)

    creation_date = models.DateTimeField(editable=False)
    update_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.creation_date = timezone.now()
        self.update_date = timezone.now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} ({self.role})'


class Institution(models.Model):
    class Status(models.TextChoices):
        INCOMPLETE = 'I', _('Not enough data to verify')
        PENDING = 'P', _('Ready, waiting for DNS check')
        VERIFIED = 'V', _('Domain verified')
        REJECTED = 'R', _('Verification failed – check domain')

    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)

    name = models.CharField(max_length=255)
    acronym = models.CharField(max_length=255, null=True, blank=True)

    phone = models.CharField(max_length=20, null=True, blank=True)

    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    full_address = models.TextField(null=True, blank=True)

    representative = models.ForeignKey(LegalRepresentative, on_delete=models.SET_NULL, related_name='institutions', null=True, blank=True)

    domain = models.CharField(max_length=255, null=True, blank=True)
    domain_verified = models.BooleanField(default=False)
    domain_verification_date = models.DateTimeField(null=True, blank=True)

    status = models.CharField(
        max_length=1,
        choices=Status.choices,
        default=Status.INCOMPLETE
    )

    creation_date = models.DateTimeField(editable=False)
    update_date = models.DateTimeField()

    @property
    def is_profile_complete(self):
        basic_data_complete = all([
            self.phone,
            self.city,
            self.state,
            self.country,
            self.full_address
        ])

        representative_complete = all([
            self.representative.name,
            self.representative.role,
            self.representative.email,
            self.representative.phone
        ]) if self.representative else False

        return basic_data_complete and representative_complete

    @property
    def is_active(self):
        return self.user.is_active

    def save(self, *args, **kwargs):
        if not self.id:
            self.creation_date = timezone.now()
        self.update_date = timezone.now()

        if self.status != self.Status.VERIFIED:
            if self.is_profile_complete:
                self.status = self.Status.PENDING
            else:
                self.status = self.Status.INCOMPLETE

        return super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username
