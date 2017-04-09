# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models


class Privacy(object):
    PUBLIC = 0
    PRIVATE = 1


class Wiki(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    version = models.IntegerField(default=0)
    privacy = models.IntegerField(default=Privacy.PUBLIC)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Version(models.Model):
    wiki = models.ForeignKey(Wiki, on_delete=models.CASCADE, related_name='versions')
    version = models.IntegerField(default=0)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-version']
