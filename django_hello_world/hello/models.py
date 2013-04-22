# coding=utf-8
from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Profile(models.Model):

    user = models.ForeignKey(User)
    birthday = models.DateField(null=True)
    bio = models.TextField(max_length=600, blank=True, null=True)
    jabber = models.CharField(max_length=60, blank=True, null=True)
    skype = models.CharField(max_length=60, blank=True, null=True)
    contacts = models.TextField(max_length=600, blank=True, null=True)



