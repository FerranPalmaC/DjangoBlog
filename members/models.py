from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.username} -- {self.email}"

    # username and email can't be the same
    def clean(self):
        if self.username == self.email:
            raise ValidationError("Username and email can't be the same. Please, provide a different username/email")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


