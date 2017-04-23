# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class ProfConfig(AppConfig):
    name = 'prof'

    def ready(self):
        from .signals import autocreate_user_options
