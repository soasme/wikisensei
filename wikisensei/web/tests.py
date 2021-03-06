# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from wikisensei.wiki.services import get_root_wiki
from wikisensei.wiki.services import add_wiki
from wikisensei.subscription.services import subscribe_without_plan

class WebTestCase(TestCase):

    fixtures = [
        'wikisensei/stubs/test_user.json',
    ]

    def test_user_can_visit_root_wiki_after_login(self):
        # login
        self.client.login(username='test', password='abcd.1234')

        # access wiki root page
        response = self.client.get(reverse('wiki_root'))
        self.assertEqual(response.status_code, 200)


    def test_user_cannot_visit_root_wiki_if_user_not_login(self):
        # access wiki root page
        response = self.client.get(reverse('wiki_root'))
        self.assertEqual(response.status_code, 403)


    def test_user_can_update_root_wiki(self):
        # login
        response = self.client.login(username='test', password='abcd.1234')
        wiki = get_root_wiki(User.objects.get(username='test'))

        # access update page
        response = self.client.get(reverse('wiki_update', kwargs={'pk': wiki.pk}))
        self.assertEqual(response.status_code, 200)

        # update form
        data = {'title': 'Home', 'content': 'Hello World!!!', 'privacy': 'public'}
        response = self.client.post(reverse('wiki_update', kwargs={'pk': wiki.pk}), data)
        self.assertEqual(response.status_code, 302)

        # validate successfully updated
        response = self.client.get(reverse('wiki_update', kwargs={'pk': wiki.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['wiki'], wiki)


    def test_user_can_create_wikis_from_root_wiki(self):
        # login
        response = self.client.login(username='test', password='abcd.1234')
        user = User.objects.get(username='test')
        subscribe_without_plan(user)
        wiki = get_root_wiki(user)

        # update form
        data = {
            'title': 'Home',
            'content': '[[New Page]] [[New Page]] [[Another Page|Another]]',
            'privacy': 'public',
        }
        response = self.client.post(reverse('wiki_update', kwargs={'pk': wiki.pk}), data)
        self.assertEqual(response.status_code, 302)

        # visit my wiki list, 3 pages should be there.
        response = self.client.get(reverse('wiki_list'))
        serializer = response.context['serializer']
        self.assertEqual(['Home', 'New Page', 'Another'],
                         [i['title'] for i in serializer.data])

    def test_user_can_delete_wiki(self):
        # login
        response = self.client.login(username='test', password='abcd.1234')
        wiki = add_wiki(User.objects.get(username='test'), 'Test', 'Hello World')

        # delete wiki
        response = self.client.post(reverse('wiki_delete', kwargs={'pk': wiki.pk}))
        response = self.client.get(reverse('wiki_show', kwargs={'pk': wiki.pk}))
        assert response.status_code == 404

    def test_user_cannot_delete_root_wiki(self):
        # login
        response = self.client.login(username='test', password='abcd.1234')
        wiki = get_root_wiki(User.objects.get(username='test'))

        # delete root wiki
        response = self.client.post(reverse('wiki_delete', kwargs={'pk': wiki.pk}))
        response = self.client.get(reverse('wiki_show', kwargs={'pk': wiki.pk}))
        assert response.status_code == 200


    def test_user_create_private_wiki(self):
        # login
        response = self.client.login(username='test', password='abcd.1234')
        wiki = get_root_wiki(User.objects.get(username='test'))

        # update form
        data = {
            'title': 'Home',
            'content': 'Hello World',
            'privacy': 'private',
        }
        response = self.client.post(reverse('wiki_update', kwargs={'pk': wiki.pk}), data)
        self.assertEqual(response.status_code, 302)

        self.client.logout()
        self.client.login(username='admin', password='abcd.1234')
        response = self.client.get(reverse('user_wiki_home', kwargs=dict(username='test')))
        self.assertEqual(response.status_code, 403)

    def test_user_cannot_update_wiki_title_to_existed_wiki_title(self):
        pass

    ### Profile Setting

    def test_user_can_update_profile_setting(self):
        # login
        response = self.client.login(username='test', password='abcd.1234')
        user = User.objects.get(username='test')

        # set private wiki
        response = self.client.post(reverse('account_profile'), data={
            'private_wiki': True,
            'private_email': False,
        })
        self.assertEqual(response.status_code, 302)

        # check setting
        response = self.client.get(reverse('account_profile'))
        serializer = response.context['serializer']
        self.assertTrue(serializer.data['private_wiki'])
        self.assertFalse(serializer.data['private_email'])

        self.client.logout()
        self.client.login(username='admin', password='abcd.1234')
        response = self.client.get(reverse('user_wiki_home', kwargs=dict(username='test')))
        self.assertEqual(response.status_code, 403)
