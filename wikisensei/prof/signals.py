# -*- coding: utf-8 -*-

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Option

@receiver(post_save, sender=User)
def autocreate_user_options(sender, instance, **kwargs):
    if not instance.created:
        return
    option = Option(user=instance, private_email=True, private_wiki=False)
    # FIXME: duplication error, ignore
    option.save()
