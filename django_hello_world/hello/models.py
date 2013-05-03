# coding=utf-8
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.db import models


class Profile(models.Model):

    user = models.ForeignKey(User)
    first_name = models.CharField(verbose_name=_('Name'), max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    photo = models.ImageField(blank=True, upload_to='photos', default='')
    birthday = models.DateField(null=True)
    bio = models.TextField(max_length=600, blank=True, null=True)
    jabber = models.CharField(max_length=60, blank=True, null=True)
    skype = models.CharField(max_length=60, blank=True, null=True)
    contacts = models.TextField(max_length=600, blank=True, null=True)

    def __unicode__(self):
        return 'Profile "%s"' % self.user.username


class StoredHttpRequest(models.Model):

    user = models.ForeignKey(User, null=True)
    date = models.DateTimeField(default=timezone.now)
    method = models.CharField(max_length=10, blank=False, null=False)
    is_secure = models.BooleanField(null=False)
    full_path = models.TextField(max_length=500, blank=False, null=False)
    user_agent = models.TextField(max_length=300, blank=False, null=True)
    referer = models.TextField(max_length=300, blank=False, null=True)
    remote_addr = models.GenericIPAddressField()
    priority = models.IntegerField(db_index=True, default=0)

    def __unicode__(self):
        return '%s %s' % (self.method, self.full_path)

    class Meta:
        ordering = ['-priority', 'id']
