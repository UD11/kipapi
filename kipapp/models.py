from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.EmailField()
    enrollment_number = models.CharField(max_length=20)
    passout_year = models.CharField(max_length=20)
    state = models.CharField(max_length=10)
    department = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username


