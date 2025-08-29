import hashlib
import os

from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from institution.models import Institution
from subject.models import Subject


def directory_path(instance, filename):
    name, extension = os.path.splitext(filename)
    safe_name = slugify(name)
    institution_slug = slugify(instance.institution.name)

    hash = hashlib.md5(f'{filename}{instance.subject.id}{instance.institution.id}'.encode()).hexdigest()

    final_filename = f'{safe_name}_{hash[:8]}{extension}'
    return f'documents/{institution_slug}/{final_filename}'


class Document(models.Model):
    file = models.FileField(upload_to=directory_path)
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT, related_name='documents')
    institution = models.ForeignKey(Institution, on_delete=models.PROTECT, related_name='documents')

    ipfs_cid = models.CharField(max_length=255, blank=True, null=True)

    upload_date = models.DateTimeField(editable=False)
    update_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.upload_date = timezone.now()
        self.update_date = timezone.now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return os.path.basename(self.file.name)
