# -*- coding: utf-8 -*-

import json
from copy import deepcopy
from glob import glob

import wikisensei.settings
from django.core import management
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Reset dev data in database.'

    def handle(self, *args, **options):
        if not wikisensei.settings.DEBUG:
            raise Exception('Not allowed executing this command in DEBUG mode.')
        for app in wikisensei.settings.INSTALLED_APPS:
            try:
                management.call_command('migrate', app, 'zero')
            except Exception as e:
                pass
        management.call_command('migrate')
        management.call_command('flush', verbosity=1, interactive=False)
        management.call_command('add_stub')
        management.call_command('sync_plans')
        management.call_command('init_customers')
