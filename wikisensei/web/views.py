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
from django.http import HttpResponseForbidden

from rest_framework import generics
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import ListModelMixin
from rest_framework.pagination import PageNumberPagination
from wikisensei.wiki.models import Wiki
from wikisensei.wiki.models import Version
from wikisensei.wiki.serializers import WikiSerializer
from wikisensei.wiki.serializers import RevisionSerializer
from wikisensei.wiki.services import get_root_wiki
from wikisensei.wiki.services import is_private
from wikisensei.wiki.services import get_next_wiki
from wikisensei.wiki.services import delete_wiki
from wikisensei.wiki.services import is_root_wiki
from wikisensei.wiki.services import validate_root_wiki_title
from wikisensei.wiki.services import ROOT_WIKI_TITLE

from wikisensei.prof.serializers import ProfileSettingSerializer
from wikisensei.prof.serializers import CustomStyleSerializer
from wikisensei.prof.services import get_custom_style

from .permissions import ViewPrivateWikiPermission
from .permissions import SubscriptionRequiredPermission

def index(request):
    if request.user.is_authenticated:
        return redirect('account_profile')
    else:
        return redirect('account_login')

def price(request):
    return render(request, 'site/price.html')

def help(request):
    return render(request, 'site/help.html')


class WikiDetail(APIView):
    page_title = None
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'wiki/show.html'
    permission_classes = (
        ViewPrivateWikiPermission,
    )

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

    def get(self, request, pk, version=None):
        wiki = get_object_or_404(Wiki, pk=pk)
        version = version or wiki.version

        # check permission
        self.check_object_permissions(request, wiki)

        # handle next
        res = self.route_next(request, wiki)
        if res:
            return res

        serializer = WikiSerializer(wiki, context={'version': version})

        return Response({
            'serializer': serializer,
            'wiki': wiki,
            'style': get_custom_style(wiki.user),
            'title': self.page_title or wiki.title,
        })



class WikiCreate(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'wiki/create.html'
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (
        IsAuthenticated,
        SubscriptionRequiredPermission,
    )

    def get(self, request):
        serializer = WikiSerializer(data={
            'title': '',
            'content': '',
            'privacy': 'public'
        })
        serializer.is_valid()
        return Response({
            'serializer': serializer
        })

    def post(self, request):
        data = {
            'title': request.data.get('title'),
            'content': request.data.get('content'),
            'private': request.data.get('privacy'),
        }
        serializer = WikiSerializer(data=data)
        if not serializer.is_valid():
            return Response({
                'serializer': serializer,
            })
        serializer.save(user=request.user)
        return redirect('wiki_show', pk=serializer.data.get('id'))

class WikiRevisionsPagination(PageNumberPagination):
    page_size = 50

class WikiRevisions(generics.ListAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'wiki/revisions.html'
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    serializer_class = RevisionSerializer
    model = serializer_class.Meta.model
    pagination_class = WikiRevisionsPagination
    permission_classes = (
        IsAuthenticated,
        ViewPrivateWikiPermission,
        SubscriptionRequiredPermission,
    )

    def get_object(self):
        view, args, kwargs = self.request.resolver_match
        pk = kwargs['pk']
        wiki = get_object_or_404(Wiki, pk=pk)
        self.check_object_permissions(self.request, wiki)
        return wiki

    def get_queryset(self):
        wiki = self.get_object()
        queryset = self.model.objects.filter(wiki=wiki)
        return queryset.order_by('-version')

    def list(self, request, **kwargs):
        response = super(WikiRevisions, self).list(request)
        return Response({
            'revisions': response.data
        })


class WikiRevision(WikiDetail):
    permission_classes = (
        ViewPrivateWikiPermission,
        SubscriptionRequiredPermission,
    )

    def get(self, request, pk, version):
        wiki = get_object_or_404(Wiki, pk=pk)
        version = int(version)
        if version > wiki.version:
            raise Http404()
        return super(WikiRevision, self).get(request, pk, version)


class WikiUpdate(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'wiki/update.html'
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (
        IsAuthenticated,
        ViewPrivateWikiPermission,
    )

    def get(self, request, pk):
        wiki = get_object_or_404(Wiki, pk=pk)
        self.check_object_permissions(request, wiki)
        serializer = WikiSerializer(wiki)
        return Response({
            'wiki': wiki,
            'serializer': serializer
        })

    def post(self, request, pk):
        wiki = get_object_or_404(Wiki, pk=pk)
        self.check_object_permissions(request, wiki)

        # user need to be author
        if wiki.user != request.user:
            raise PermissionDenied

        serializer = WikiSerializer(wiki, data=request.data)

        # validate
        if not serializer.is_valid():
            # move unique together message to title
            serializer._errors.setdefault('title', [])
            serializer._errors['title'].extend(
                serializer.errors.get(api_settings.NON_FIELD_ERRORS_KEY, [])
            )
            if api_settings.NON_FIELD_ERRORS_KEY in serializer._errors:
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
    permission_classes = (
        IsAuthenticated,
    )

    def get(self, request):
        wiki = get_root_wiki(request.user)
        return super(WikiRoot, self).get(request, wiki.pk)


class WikiList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'wiki/list.html'
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (
        IsAuthenticated,
        SubscriptionRequiredPermission,
    )

    def get(self, request):
        wikis = Wiki.objects.filter(user=request.user)
        serializer = WikiSerializer(wikis, many=True)
        return Response({
            'serializer': serializer,
        })

class SiteWikiPage(WikiDetail):
    wiki_title = ROOT_WIKI_TITLE

    def get(self, request):
        user = get_object_or_404(User, username=settings.SITE_USERNAME)
        wiki = get_object_or_404(Wiki, user=user, title=self.__class__.wiki_title)
        return super(SiteWikiPage, self).get(request, wiki.pk)

class UserWikiHome(WikiDetail):

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        wiki = get_root_wiki(user)
        return super(UserWikiHome, self).get(request, wiki.pk)

class Home(SiteWikiPage):
    wiki_title = 'Home'
    page_title = 'Tomato'

class Price(SiteWikiPage):
    wiki_title = 'Price'

class Help(SiteWikiPage):
    wiki_title = 'Help'

class Profile(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'accounts/profile.html'
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        option = ProfileSettingSerializer.get_option_by_user(request.user)
        serializer = ProfileSettingSerializer(option, data={})
        serializer.is_valid()
        return Response({
            'serializer': serializer
        })

    def post(self, request):
        option = ProfileSettingSerializer.get_option_by_user(request.user)
        serializer = ProfileSettingSerializer(option, data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
        return redirect('account_profile')

class CustomStyle(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'accounts/custom_style.html'
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (
        IsAuthenticated,
        SubscriptionRequiredPermission,
    )

    def get(self, request):
        style = get_custom_style(request.user)
        serializer = CustomStyleSerializer(style, data={'css': style.css or ''})
        serializer.is_valid()
        return Response({
            'serializer': serializer,
        })

    def post(self, request):
        style = get_custom_style(request.user)
        serializer = CustomStyleSerializer(style, data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
        return redirect('account_custom_style')

class WikiDelete(WikiDetail):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (
        IsAuthenticated,
        ViewPrivateWikiPermission,
    )

    def post(self, request, pk):
        wiki = get_object_or_404(Wiki, pk=pk)

        # check permission
        self.check_object_permissions(request, wiki)

        delete_wiki(wiki)

        return redirect('home')
