# -*- coding: utf-8 -*-

import json
from copy import deepcopy
from glob import glob

from django.core import management
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Reset dev data in database.'

    def handle(self, *args, **options):
        management.call_command('migrate')
        management.call_command('flush', verbosity=1, interactive=False)
        management.call_command('add_stub')
