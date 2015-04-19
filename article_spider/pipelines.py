# -*- coding: utf-8 -*-
import pprint

import django
from django.core.exceptions import ObjectDoesNotExist

from website.models import Athlete, Entity


class SaveArticlePipeline(object):

    MIN_RELEVANCE_LEVEL = 15

    def __init__(self):
        django.setup()
        self.athletes = Athlete.objects.all()
        assert len(self.athletes) > 0

    def process_item(self, item, spider):

        saved = 0
        updated = 0
        
        for athlete in self.athletes:

            relevance = item.get_relevance(athlete)

            if relevance > self.MIN_RELEVANCE_LEVEL:

                entity = item.format()

                entity.athlete = athlete
                entity.relevance = relevance

                try:
                    existing = Entity.objects.get(url=entity.url, athlete=athlete)

                    if entity.get_hash() != existing.hash:

                        print "%s != %s" % (entity.hash, existing.hash)
                        print "%s %s %s %s" % (existing.id, existing.title, existing.url, existing.type)

                        entity.id = existing.id
                        entity.save()
                        updated += 1

                except ObjectDoesNotExist:

                    entity.save()
                    saved += 1

        return "Saved %s / Updated %s" % (saved, updated)