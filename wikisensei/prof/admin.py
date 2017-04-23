# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Option, CustomStyle

class OptionInline(admin.StackedInline):
    model = Option
    can_delete = False
    verbose_name_plural = 'option'

class CustomStyleInline(admin.StackedInline):
    model = CustomStyle
    can_delete = False
    verbose_name_plural = 'custom_style'

class UserAdmin(BaseUserAdmin):
    inlines = (OptionInline, CustomStyleInline)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
