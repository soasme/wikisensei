# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'site/intro.html')

def create_wiki(request):
    return render(request, 'wiki/create.html')

def show_wiki(request):
    return render(request, 'wiki/show.html')

def update_wiki(request):
    return render(request, 'wiki/update.html')
