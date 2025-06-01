from django.contrib.auth.models import AbstractUser
from django.db import models


class UserTypeChoices(models.TextChoices):
    INSTITUTION = 'I', 'Institution'
    SUBJECT = 'S', 'Subject'


class VeridyUser(AbstractUser):

    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=1, choices=UserTypeChoices.choices)

    def is_institution(self):
        return self.user_type == UserTypeChoices.INSTITUTION

    def is_subject(self):
        return self.user_type == UserTypeChoices.SUBJECT

    def __str__(self):
        return self.username or self.email
