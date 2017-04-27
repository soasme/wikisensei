# -*- coding: utf-8 -*-

from django.conf import settings
from rest_framework import permissions, exceptions
from wikisensei.wiki.services import is_private as is_wiki_private
from wikisensei.prof.services import is_all_wikis_private
from wikisensei.subscription.services import get_subscription_by_user

class ViewPrivateWikiPermission(permissions.BasePermission):
    message = 'Viewing private wiki not allowed.'

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, wiki):
        is_same_user = request.user == wiki.user
        is_private = is_all_wikis_private(wiki.user) or is_wiki_private(wiki)
        if is_private and not is_same_user:
            raise exceptions.PermissionDenied(detail=self.message)
        return True

class SubscriptionRequiredPermission(permissions.BasePermission):
    message = 'Subscribed to a plan required.'

    def has_permission(self, request, view):
        # if stripe is not enabled, then we do not check this permission.
        if not settings.STRIPE.get('enabled'):
            return True

        user = request.user

        if not user.is_authenticated:
            return False

        if not get_subscription_by_user(user):
            return False

        return True
