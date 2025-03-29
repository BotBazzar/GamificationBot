from django.db import models

from db.models import Employee


class Group(models.Model):
    name = models.CharField(max_length=255)
    leader = models.ForeignKey(Employee, on_delete=models.CASCADE)


class Locations(models.Model):
    latitude = models.FloatField(max_length='20')
    longitude = models.FloatField(max_length='20')
    name = models.CharField(max_length=255)
