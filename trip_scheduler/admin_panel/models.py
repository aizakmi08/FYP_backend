# admin_panel/models.py
from django.db import models

class Trip(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    # Add more fields as needed

    def __str__(self):
        return self.title

class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    # Add more fields as needed

    def __str__(self):
        return self.username
