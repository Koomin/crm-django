from django.db import models


class ViewPermission(models.Model):
    name = models.CharField(max_length=50)
    view = models.CharField(max_length=50, unique=True)


class GroupPermission(models.Model):
    name = models.CharField(max_length=50)
    view_permissions = models.ManyToManyField(ViewPermission)
