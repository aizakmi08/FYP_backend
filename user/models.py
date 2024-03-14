from django.contrib.auth.models import AbstractUser
from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class User(models.Model):
    department_choices = (
        ("STAFF", "Staff"),
        ("FACULTY", "Faculty")
    )

    is_admin = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    department = models.CharField(choices=department_choices, max_length=20)

    def __str__(self):
        return f"{self.name} - {self.surname}"
