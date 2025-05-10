from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class LegalRepresentative(models.Model):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.role})"


class Institution(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    tax_id = models.CharField(max_length=50)
    domain = models.CharField(max_length=255, help_text="e.g., example.edu.br")
    institutional_email = models.EmailField()
    phone = models.CharField(max_length=20)

    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    full_address = models.TextField()

    representative = models.ForeignKey(LegalRepresentative, on_delete=models.CASCADE, related_name='institutions')

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
