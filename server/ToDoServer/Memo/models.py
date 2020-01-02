from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Group(models.Model):
    index = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    group_name = models.CharField(max_length=50)


class Memo(models.Model):
    index = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, models.SET_NULL, blank=True, null=True)
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    isDo = models.BooleanField(default=False)
    isStar = models.BooleanField(default=False)
    targetDate = models.DateTimeField(null=True, blank=True)
