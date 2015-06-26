# -*- coding: utf-8 -*-
import hashlib
import pprint
import re

import html2text
from scrapy.contrib.djangoitem import DjangoItem

from website.models import Entity


class EntityItem(DjangoItem):
    django_model = Entity
    entity_type = Entity.ARTICLE

    LINK_MATCH_SCORE = 25
    FULL_MATCH_SCORE = 10
    LAST_MATCH_SCORE = 2

    def format(self):
        model = self.save(commit=False)

        model.type = self.entity_type

        return model

    def get_relevance(self, athlete):

        relevance = self.get('relevance', 0)

        if re.search(athlete.name, self['title'], re.IGNORECASE) is not None:
            relevance += self.LINK_MATCH_SCORE

        return relevance


class VideoItem(EntityItem):
    django_model = Entity
    entity_type = Entity.VIDEO


class ArticleItem(EntityItem):
    django_model = Entity
    entity_type = Entity.ARTICLE

    def format(self):
        model = EntityItem.format(self)

        model.plain_text = html2text.html2text(self['content'])

        return model

    def get_relevance(self, athlete):
        relevance = EntityItem.get_relevance(self, athlete)

        last_name = athlete.name.split(' ')[1]

        full_matches = re.findall(athlete.name, self['content'], re.IGNORECASE)
        last_matches = re.findall(' ' + last_name, self['content'], re.IGNORECASE)

        relevance += (len(full_matches) * self.FULL_MATCH_SCORE) + \
                     (len(last_matches) * self.LAST_MATCH_SCORE)

        return relevance
