from django.db import models


class User(models.Model):
    chat_id = models.CharField(max_length=255)


class Employee(models.Model):
    full_name = models.CharField(max_length=255)
    employee_id = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Admin(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
