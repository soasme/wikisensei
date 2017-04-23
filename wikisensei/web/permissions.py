# -*- coding: utf-8 -*-

from rest_framework import permissions, exceptions
from wikisensei.wiki.services import is_private as is_wiki_private
from wikisensei.prof.services import is_all_wikis_private

class ViewPrivateWikiPermission(permissions.BasePermission):
    message = 'Viewing private wiki not allowed.'

    def has_object_permission(self, request, view, wiki):
        is_same_user = request.user == wiki.user
        is_private = is_all_wikis_private(request.user) or is_wiki_private(wiki)
        if is_private and not is_same_user:
            raise exceptions.PermissionDenied
        return True
