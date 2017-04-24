# -*- coding: utf-8 -*-

import mistune
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Wiki
from .models import Version
from .models import Privacy
from .services import get_wiki_content
from .services import get_wiki_revision
from .services import add_wiki
from .services import update_wiki
from .services import render_wiki_html
from .services import create_wikis_from_wiki

class RevisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Version
        fields = ('id', 'created_at', 'version', 'wiki_id', )

class WikiSerializer(serializers.Serializer):

    title = serializers.CharField(max_length=30)
    content = serializers.CharField(
        style={'base_template': 'textarea.html', 'rows': 20},
    )
    privacy = serializers.ChoiceField([
        ('private', 'Private'),
        ('public', 'Public'),
    ])

    privacy_map = {
        'private': Privacy.PRIVATE,
        'public': Privacy.PUBLIC,
    }

    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=Wiki.objects.all(),
                fields=('user', 'title'),
                message=u'You have already had another wiki with same title.',
            )
        ]

    def validate_title(self, value):
        if not value:
            raise serializers.ValidationError('Wiki title does not provide.')
        if value.startswith('['):
            raise serializers.ValidationError('Wiki title should not starts with [.')
        if ']' in value:
            raise serializers.ValidationError('Wiki title should not contain ].')
        if '|' in value:
            raise serializers.ValidationError('Wiki title should not contain |.')
        if '\n' in value:
            raise serializers.ValidationError('Wiki title should not be multiple lines.')
        return value

    def validate_content(self, value):
        if not value:
            raise serializers.ValidationError('Wiki title does not provide.')
        return value

    def create(self, validated_data):
        wiki = add_wiki(
            user=validated_data['user'],
            title=validated_data['title'],
            content=validated_data['content'],
            privacy=self.privacy_map[validated_data['privacy']],
        )
        create_wikis_from_wiki(wiki)
        return wiki

    def update(self, instance, validated_data):
        update_wiki(instance,
            title=validated_data.get('title'),
            content=validated_data.get('content'),
            privacy=self.privacy_map[validated_data['privacy']],
        )
        create_wikis_from_wiki(instance)
        return instance

    def to_representation(self, wiki):
        if self.context.get('version'):
            revision = get_wiki_revision(wiki, self.context['version'])
            content = revision.content
            updated_at = revision.created_at
        else:
            revision = get_wiki_content(wiki)
            content = revision.content
            updated_at = revision.created_at
        html = render_wiki_html(content)
        return {
            'id': wiki.id,
            'title': wiki.title,
            'content': content,
            'html': html,
            'created_at': wiki.created_at,
            'updated_at': updated_at,
        }
