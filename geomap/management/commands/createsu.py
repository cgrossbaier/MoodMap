import os

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):

    def handle(self, *args, **options):
        User.objects.filter(username="admin").delete()
        if not User.objects.filter(username="admin").exists():
            user = User.objects.create_superuser("admin", "admin@admin.com", "admin")
            user.save()
            




