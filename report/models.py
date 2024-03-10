from django.db import models
from user.models import Department


# Create your models here.
class Report(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    total_distance = models.FloatField()

    def __str__(self):
        return f"Report for {self.department.name}"
