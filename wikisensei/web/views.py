# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

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
