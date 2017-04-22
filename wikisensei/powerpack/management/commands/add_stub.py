# -*- coding: utf-8 -*-

import json
from copy import deepcopy
from glob import glob

from django.apps import apps
from django.utils.termcolors import colorize
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Add stub data for language.'

    def handle(self, *args, **options):
        for filename in glob('./wikisensei/stubs/*.json'):
            if 'test_' in filename:
                print(colorize(text='Ignore %s' % filename, fg='yellow'))
                continue
            else:
                print(colorize(text=filename, fg='cyan'))
            with open(filename) as f:
                data = f.read()
                data = json.loads(data)
                app_label = data['app_label']
                for instance_data in data['instances']:
                    model_name = instance_data['model_name']
                    model = apps.get_model(app_label, model_name)
                    queryset_data = deepcopy(instance_data['data'])
                    for ref in instance_data.get('refs', []):
                        ref_app_label = instance_data['refs'][ref].get('app_label', app_label)
                        ref_model_name = instance_data['refs'][ref]['model_name']
                        ref_model = apps.get_model(ref_app_label, ref_model_name)
                        ref_instance = ref_model.objects.get(**instance_data['refs'][ref]['data'])
                        queryset_data[ref] = ref_instance
                    try:
                        instance = model.objects.get(**queryset_data)
                        print(u'✓ %s %s' % (instance, colorize('OK', fg='green')))
                    except model.DoesNotExist:
                        instance = model.objects.create(**queryset_data)
                        print(u'+ %s %s' % (instance, colorize('OK', fg='green')))
