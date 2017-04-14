# -*- coding: utf-8 -*-

import mistune
from rest_framework import serializers

from .models import Wiki
from .services import get_wiki_content
from .services import add_wiki
from .services import update_wiki
from .services import render_wiki_html

class WikiSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=30)
    content = serializers.CharField(
        style={'base_template': 'textarea.html', 'rows': 20},
    )

    def validate_title(self, value):
        if not value:
            raise serializers.ValidationError('Wiki title does not provide.')
        if value.startswith('['):
            raise serializers.ValidationError('Wiki title should not starts with [.')
        if ']' in value:
            raise serializers.ValidationError('Wiki title should not contain ].')
        if '\n' in value:
            raise serializers.ValidationError('Wiki title should not be multiple lines.')
        return value

    def validate_content(self, value):
        if not value:
            raise serializers.ValidationError('Wiki title does not provide.')
        return value

    def create(self, validated_data):
        return add_wiki(
            user=validated_data['user'],
            title=validated_data['title'],
            content=validated_data['content'],
        )

    def update(self, instance, validated_data):
        update_wiki(instance,
            title=validated_data.get('title'),
            content=validated_data.get('content')
        )
        return instance

    def to_representation(self, wiki):
        content = get_wiki_content(wiki).content
        html = render_wiki_html(content)
        return {
            'id': wiki.id,
            'title': wiki.title,
            'content': content,
            'html': html,
            'created_at': wiki.created_at,
            'updated_at': wiki.updated_at,
        }
