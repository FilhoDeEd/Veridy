import json
import os

from common.models import UserTypeChoices
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from subject.models import Subject


UserModel = get_user_model()


class Command(BaseCommand):
    help = 'Creates admin users from a JSON file'

    def handle(self, *args, **options):
        json_path = settings.ADMIN_USERS_PATH

        if not os.path.exists(json_path):
            raise CommandError(f'File not found: {json_path}')

        with open(json_path, 'r') as file:
            try:
                users = json.load(file)
            except json.JSONDecodeError as e:
                raise CommandError(f'Invalid JSON: {e}')

        for entry in users:
            username = entry.get('username')
            email = entry.get('email')
            password = entry.get('password')
            full_name = entry.get('full_name')

            if not all([username, email, password, full_name]):
                self.stderr.write(
                    self.style.ERROR(f'Missing required fields: {entry}')
                )
                continue

            if UserModel.objects.filter(username=username).exists():
                self.stdout.write(
                    self.style.WARNING(f'User "{username}" already exists. Skipped.')
                )
                continue

            try:
                with transaction.atomic():
                    user = UserModel.objects.create_superuser(
                        username=username,
                        email=email,
                        password=password,
                        user_type=UserTypeChoices.SUBJECT
                    )

                    Subject.objects.create(
                        user=user,
                        full_name=full_name
                    )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Failed to create admin user "{username}": {e}')
                )
                continue

            self.stdout.write(
                self.style.SUCCESS(f'Admin user "{username}" created successfully.')
            )
