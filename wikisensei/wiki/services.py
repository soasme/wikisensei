# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import F
from django.core.paginator import Paginator

from .models import Wiki, Version, Privacy

def add_wiki(user, title, content):
    wiki = Wiki(user=user, title=title, version=1)
    wiki.save()
    content = Version(wiki=wiki, version=1, content=content)
    content.save()
    return wiki

def update_wiki(wiki, content):
    version_num = wiki.versions.all()[0].version
    next_version_num = version_num + 1
    version = Version(wiki=wiki, version=next_version_num, content=content)
    version.save()
    wiki.version = next_version_num
    wiki.save()
    return wiki

def get_wiki_content(wiki):
    version_num = wiki.version
    versions = wiki.versions
    assert wiki.versions.count() >= 1, 'Wiki content has at least one version.'
    content = versions.get(version=version_num)
    return content

def make_wiki_public(wiki):
    wiki.privacy = Privacy.PUBLIC
    wiki.save()

def make_wiki_private(wiki):
    wiki.privacy = Privacy.PRIVATE
    wiki.save()

def is_public(wiki):
    return wiki.privacy == Privacy.PUBLIC

def is_private(wiki):
    return wiki.privacy == Privacy.PRIVATE

def get_root_wiki(user):
    wiki = Wiki.objects.filter(user=user).order_by('created_at').first()
    assert bool(wiki), 'User should have root wiki.'
    return wiki
