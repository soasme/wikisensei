# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from . import services

class WikiTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='Alice', email='alice@wikisensei.com', password='ILoveBob'
        )
        self.wiki = services.add_wiki(self.user, 'Title', 'Content')

    def test_add_wiki(self):
        self.assertEqual(self.wiki.version, 1)
        self.assertEqual(self.wiki.title, 'Title')
        self.assertEqual(services.get_wiki_content(self.wiki).content, 'Content')
        self.assertEqual(services.mget_pk_by_titles({'Title', }), {'Title': self.wiki.pk})

    def test_update_wiki(self):
        services.update_wiki(self.wiki, 'title', u'New Content 中文')
        self.assertEqual(self.wiki.version, 2)
        self.assertEqual(services.get_wiki_content(self.wiki).content, u'New Content 中文')

    def test_update_wiki_content_with_long_long_title(self):
        services.update_wiki(self.wiki, 'title', '[[%s]]' % ('a' * 1000))
        assert services.mget_pk_by_titles({'a' * 1000}) == {}

    def test_wiki_privacy(self):
        services.make_wiki_private(self.wiki)
        self.assertFalse(services.is_public(self.wiki))
        self.assertTrue(services.is_private(self.wiki))

        services.make_wiki_public(self.wiki)
        self.assertTrue(services.is_public(self.wiki))
        self.assertFalse(services.is_private(self.wiki))

    def test_extract_wiki_titles(self):
        self.assertEqual(services.extract_wiki_titles('[[hello]] [[world]]'), {'hello', 'world'})
