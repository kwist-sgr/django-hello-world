# coding=utf-8
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models


class Profile(models.Model):

    user = models.ForeignKey(User)
    birthday = models.DateField(null=True)
    bio = models.TextField(max_length=600, blank=True, null=True)
    jabber = models.CharField(max_length=60, blank=True, null=True)
    skype = models.CharField(max_length=60, blank=True, null=True)
    contacts = models.TextField(max_length=600, blank=True, null=True)


class StoredHttpRequest(models.Model):

    user = models.ForeignKey(User, null=True)
    date = models.DateTimeField(default=timezone.now)
    method = models.CharField(max_length=10, blank=False, null=False)
    is_secure = models.BooleanField(null=False)
    full_path = models.TextField(max_length=500, blank=False, null=False)
    user_agent = models.TextField(max_length=300, blank=False, null=True)
    referer = models.TextField(max_length=300, blank=False, null=True)
    remote_addr = models.GenericIPAddressField()
