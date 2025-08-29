from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


UserModel = get_user_model()


class Subject(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)

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
