# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django_extensions.admin import ForeignKeyAutocompleteAdmin

from .models import Wiki, Version

class WikiAdmin(ForeignKeyAutocompleteAdmin):
    pass

class VersionAdmin(ForeignKeyAutocompleteAdmin):
    pass

admin.site.register(Wiki, WikiAdmin)
admin.site.register(Version, VersionAdmin)
