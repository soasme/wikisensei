# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

import mistune
from django.db.models import F
from django.core.paginator import Paginator
from django.urls import reverse

from .models import Wiki, Version, Privacy

def add_wiki(user, title, content):
    wiki = Wiki(user=user, title=title, version=1)
    wiki.save()
    content = Version(wiki=wiki, version=1, content=content)
    content.save()
    return wiki

def update_wiki(wiki, title, content):
    latest_version = wiki.versions.first()
    assert latest_version, 'Wiki has at least one version.'

    next_version_num = latest_version.version

    if latest_version.content != content:
        next_version_num = next_version_num + 1
        new_version = Version(wiki=wiki, version=next_version_num, content=content)
        new_version.save()

    if wiki.title != title or wiki.version != next_version_num:
        wiki.title = title
        wiki.version = next_version_num
        wiki.save()

    return wiki

def get_wiki_content(wiki):
    version_num = wiki.version
    versions = wiki.versions
    assert wiki.versions.count() >= 1, 'Wiki content has at least one version.'
    content = versions.get(version=version_num)
    return content

def render_wiki_html(content):
    titles = extract_wiki_titles(content)
    pks = mget_pk_by_titles(titles)
    links = '\n'.join([
        '[%s]: %s' % (title, reverse('wiki_show', kwargs=dict(pk=pk)))
        for title, pk in pks.items()
    ])
    html = mistune.markdown(content + '\n' + links)
    html = html.replace('\n', '<br>')
    return html

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

def mget_pk_by_titles(titles):
    wikis = Wiki.objects.filter(title__in=list(titles))
    return {wiki.title: wiki.pk for wiki in wikis}

def extract_wiki_titles(content):
    # '[^!]?' => It should not start with ! => It's not an image link
    # \[ => It should start with [
    # ([^]]?) => It should match title as group.
    # \] => It should follow by ]
    # (?!\([^)]*\)) => It should not follow (LINK) => It's not an external link.
    return re.findall(r'[^!]?\[([^]]+?)\](?!\([^)]*\))', content)
