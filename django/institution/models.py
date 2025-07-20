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

    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
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
    phone = models.CharField(max_length=20, null=True, blank=True)

    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    full_address = models.TextField(null=True, blank=True)

    representative = models.ForeignKey(LegalRepresentative, on_delete=models.SET_NULL, related_name='institutions', null=True, blank=True)

    domain = models.CharField(max_length=255, null=True, blank=True)
    verified = models.BooleanField(default=False)

    status = models.CharField(
        max_length=1,
        choices=Status.choices,
        default=Status.INCOMPLETE
    )

    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField()

    @property
    def is_active(self):
        return self.user.is_active

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username
