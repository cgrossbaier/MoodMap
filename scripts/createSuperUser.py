from django.contrib.auth.models import User

User.objects.filter(username="admin").delete()
user = User.objects.create_superuser("admin", "admin@admin.com", "admin")
user.save()