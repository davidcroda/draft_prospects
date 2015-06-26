# -*- coding: utf-8 -*-
import copy
import logging
import pprint

import django
from django.core.exceptions import ObjectDoesNotExist

from website.models import Athlete, Entity


class SaveArticlePipeline(object):

    MIN_RELEVANCE_LEVEL = 15

    def __init__(self):
        django.setup()
        self.log = logging.getLogger('django')
        self.athletes = Athlete.objects.all()
        assert len(self.athletes) > 0

    def process_item(self, item, spider):

        saved = 0
        updated = 0
        
        for athlete in self.athletes:

            relevance = item.get_relevance(athlete)

            if relevance > self.MIN_RELEVANCE_LEVEL:

                item_copy = copy.copy(item)

                entity = item_copy.format()

                entity.athlete = athlete
                entity.relevance = relevance

                try:

                    existing = Entity.objects.get(url=entity.url, athlete_id=athlete.id)

                    if entity.get_hash() != existing.hash:

                        print "UPDATED: %s / %s" % (athlete.name, entity.url)

                        entity.id = existing.id
                        entity.save()
                        updated += 1

                except ObjectDoesNotExist:

                    print "NEW: %s / %s" % (athlete.name,entity.url)

                    entity.save()
                    saved += 1