# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Option

class OptionInline(admin.StackedInline):
    model = Option
    can_delete = False
    verbose_name_plural = 'option'

class UserAdmin(BaseUserAdmin):
    inlines = (OptionInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
