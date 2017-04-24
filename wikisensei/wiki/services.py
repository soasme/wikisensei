# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

import mistune
from django.db.models import F
from django.core.paginator import Paginator
from django.urls import reverse

from .models import Wiki, Version, Privacy
from .markdown import Parser

ROOT_WIKI_TITLE = 'Home'

def add_wiki(user, title, content, privacy=Privacy.PUBLIC):
    wiki = Wiki(user=user, title=title, version=1, privacy=privacy)
    wiki.save()
    content = Version(wiki=wiki, version=1, content=content)
    content.save()
    return wiki

def update_wiki(wiki, title, content):
    latest_version = wiki.versions.first()
    assert latest_version, 'Wiki has at least one version.'

    if is_root_wiki(wiki) and title != ROOT_WIKI_TITLE:
        raise Exception('Root wiki cannot change title.')

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
    parser = Parser()
    html = parser(content)
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

def is_root_wiki(wiki):
    return wiki.title == ROOT_WIKI_TITLE

def validate_root_wiki_title(wiki, title):
    return is_root_wiki(wiki) and title == ROOT_WIKI_TITLE

def get_root_wiki(user):
    wiki = Wiki.objects.filter(user=user).order_by('created_at').first()
    if not wiki:
        wiki = create_root_wiki(user)
    return wiki

def create_root_wiki(user):
    # FIXME: provide default content
    content = 'Kia ora!'
    return add_wiki(user, ROOT_WIKI_TITLE, content)

def get_next_wiki(wiki, title):
    try:
        return Wiki.objects.get(user=wiki.user, title=title)
    except Wiki.DoesNotExist:
        pass

def mget_pk_by_titles(titles):
    wikis = Wiki.objects.filter(title__in=list(titles))
    return {wiki.title: wiki.pk for wiki in wikis}

def extract_wiki_titles(content):
    parser = Parser()
    parser(content)
    return parser.inline.wiki_links

def create_wikis_from_wiki(wiki):
    titles = extract_wiki_titles(get_wiki_content(wiki).content)
    pks = mget_pk_by_titles(titles)
    nowiki_titles = set(titles) - set(pks.keys())
    return [
        add_wiki(wiki.user, title, 'To be continued.')
        for title in nowiki_titles
    ]
