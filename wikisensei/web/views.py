# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import Http404

from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from wikisensei.wiki.models import Wiki
from wikisensei.wiki.serializers import WikiSerializer
from wikisensei.wiki.services import get_root_wiki
from wikisensei.wiki.services import is_private
from wikisensei.wiki.services import get_next_wiki
from wikisensei.wiki.services import is_root_wiki
from wikisensei.wiki.services import validate_root_wiki_title
from wikisensei.wiki.services import ROOT_WIKI_TITLE

def index(request):
    if request.user.is_authenticated:
        return redirect('account_profile')
    else:
        return redirect('account_login')

def price(request):
    return render(request, 'site/price.html')

def help(request):
    return render(request, 'site/help.html')

@login_required
def profile(request):
    return render(request, 'accounts/profile.html', {
        'user': request.user,
    })


class WikiDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'wiki/show.html'

    def route_next(self, request, wiki):
        next_title = request.GET.get('next')

        # case: do nothing if no next.
        if not next_title:
            return

        # case: Raise 404 if no title matched.
        # This might be caused by user removing a wiki.
        wiki = get_next_wiki(wiki, next_title)
        if not wiki:
            raise Http404

        # case: Redirect to root if it's root wiki.
        if is_root_wiki(wiki):
            return redirect('wiki_root')

        # case: Redirect to wiki.
        return redirect('wiki_show', pk=wiki.pk)

    def get(self, request, pk):
        wiki = get_object_or_404(Wiki, pk=pk)

        # handle next
        res = self.route_next(request, wiki)
        if res:
            return res

        # private wiki can only be seen by author.
        if is_private(wiki) and wiki.user != request.user:
            raise PermissionDenied

        serializer = WikiSerializer(wiki)

        return Response({
            'serializer': serializer,
            'wiki': wiki,
        })

class WikiCreate(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'wiki/create.html'
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = WikiSerializer(data={
            'title': '',
            'content': ''
        })
        serializer.is_valid()
        return Response({
            'serializer': serializer
        })

    def post(self, request):
        data = {
            'title': request.data.get('title'),
            'content': request.data.get('content'),
        }
        serializer = WikiSerializer(data=data)
        if not serializer.is_valid():
            return Response({
                'serializer': serializer,
            })
        serializer.save(user=request.user)
        return redirect('wiki_show', pk=serializer.data.get('id'))

class WikiUpdate(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'wiki/update.html'
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        wiki = get_object_or_404(Wiki, pk=pk)
        if wiki.user != request.user:
            raise PermissionDenied
        serializer = WikiSerializer(wiki)
        return Response({
            'wiki': wiki,
            'serializer': serializer
        })

    def post(self, request, pk):
        wiki = get_object_or_404(Wiki, pk=pk)

        # user need to be author
        if wiki.user != request.user:
            raise PermissionDenied

        data = {
            'title': request.data.get('title'),
            'content': request.data.get('content'),
        }
        serializer = WikiSerializer(wiki, data=data)

        # validate
        if not serializer.is_valid():
            # move unique together message to title
            serializer._errors.setdefault('title', [])
            serializer._errors['title'].extend(
                serializer.errors.get(api_settings.NON_FIELD_ERRORS_KEY, [])
            )
            del serializer._errors[api_settings.NON_FIELD_ERRORS_KEY]
            return Response({
                'wiki': wiki,
                'serializer': serializer,
            })

        # save
        serializer.save(user=request.user)
        return redirect('wiki_show', pk=serializer.data.get('id'))

class WikiRoot(WikiDetail):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        wiki = get_root_wiki(request.user)
        return super(WikiRoot, self).get(request, wiki.pk)


class WikiList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'wiki/list.html'
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        wikis = Wiki.objects.filter(user=request.user)
        serializer = WikiSerializer(wikis, many=True)
        return Response({
            'serializer': serializer,
        })

class WikiPage(WikiDetail):
    page_title = ROOT_WIKI_TITLE

    def get(self, request):
        user = get_object_or_404(User, username=settings.SITE_USERNAME)
        wiki = get_object_or_404(Wiki, user=user, title=self.__class__.page_title)
        return super(WikiPage, self).get(request, wiki.pk)

class UserWikiHome(WikiDetail):

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        wiki = get_root_wiki(user)
        return super(UserWikiHome, self).get(request, wiki.pk)

class Home(WikiPage):
    page_title = 'Home'

class Price(WikiPage):
    page_title = 'Price'

class Help(WikiPage):
    page_title = 'Help'
