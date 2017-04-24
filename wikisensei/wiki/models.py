# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.db import models


class Privacy(object):
    PUBLIC = 0
    PRIVATE = 1


class Wiki(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    version = models.IntegerField(default=0)
    hash = models.CharField(max_length=32, null=True)
    privacy = models.IntegerField(default=Privacy.PUBLIC)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'title', )

    def __unicode__(self):
        return u'%s/%s' % (self.user.username, self.title)


class Version(models.Model):
    wiki = models.ForeignKey(Wiki, on_delete=models.CASCADE, related_name='versions')
    version = models.IntegerField(default=0)
    content = models.TextField()
    compiled = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    compiled_at = models.DateTimeField(null=True)

    class Meta:
        ordering = ['-version']

    def __unicode__(self):
        return u'%d!%s...' % (self.version, self.content[:10])
