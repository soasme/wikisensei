# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from wikisensei.wiki.models import Wiki
from wikisensei.wiki.serializers import WikiSerializer
from wikisensei.wiki.services import get_root_wiki

def index(request):
    return render(request, 'site/intro.html')

@login_required
def profile(request):
    return render(request, 'accounts/profile.html', {
        'user': request.user,
    })

@login_required
def create_wiki(request):
    return render(request, 'wiki/create.html')

@login_required
def show_wiki(request, username, title):
    data = {'content': '<h1>hello world</h1>'}
    return render(request, 'wiki/show.html', data)

@login_required
def update_wiki(request):
    return render(request, 'wiki/update.html')


class WikiDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'wiki/show.html'

    def get(self, request, pk):
        wiki = get_object_or_404(Wiki, pk=pk)
        serializer = WikiSerializer(wiki)
        return Response({
            'serializer': serializer,
            'wiki': wiki,
        })

class WikiCreate(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'wiki/create.html'

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

    def get(self, request, pk):
        wiki = get_object_or_404(Wiki, pk=pk)
        serializer = WikiSerializer(wiki)
        return Response({
            'serializer': serializer
        })

    def post(self, request, pk):
        data = {
            'title': request.data.get('title'),
            'content': request.data.get('content'),
        }
        wiki = get_object_or_404(Wiki, pk=pk)
        serializer = WikiSerializer(wiki, data=data)
        if not serializer.is_valid():
            return Response({
                'serializer': serializer,
            })
        serializer.save(user=request.user)
        return redirect('wiki_show', pk=serializer.data.get('id'))

class WikiRoot(APIView):

    def get(self, request):
        wiki = get_root_wiki(request.user)
        return redirect('wiki_show', pk=wiki.pk)
