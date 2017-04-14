# -*- coding: utf-8 -*-

from .services import add_wiki

def create_root_wiki(sender, **kwargs):
    user = kwargs['user']
    # FIXME: provide default content
    content = 'Hello World'
    add_wiki(user, 'Home', content)

