# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Option(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    private_email = models.BooleanField(default=False)
    private_wiki = models.BooleanField(default=False)

class CustomStyle(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    css = models.TextField()
