# -*- coding: utf-8 -*-
import django
from django.core.exceptions import ObjectDoesNotExist
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
import re
from website.models import Athlete, Video


class DraftExpressSpider(CrawlSpider):

    name = "draftexpress"
    allowed_domains = ["draftexpress.com"]
    start_urls = (
        'http://www.draftexpress.com/videos/Scouting/',
    )

    rules = (
        Rule(LxmlLinkExtractor(allow='/videos/[0-9]+'), callback='parse_video'),
    )

    athletes = ()

    LINK_MATCH_SCORE = 50
    FULL_MATCH_SCORE = 10
    LAST_MATCH_SCORE = 2
    MIN_RELEVANCE_LEVEL = 10

    def __init__(self):
        super(DraftExpressSpider, self).__init__()
        self.athletes = Athlete.objects.all()
        django.setup()
        assert len(self.athletes) > 0


    def parse_video(self, response):

        for athlete in self.athletes:

            if re.search(athlete.name, response.meta['link_text'], re.IGNORECASE):

                pbid = re.search(r'player.ooyala.com\/v[0-9]+\/([a-z0-9]*32?)"', response.body).group(1)
                ec = re.search(r'\{cId: "([a-zA-Z0-9]*?)"',response.body).group(1)
                link = "http://player.ooyala.com/iframe.html#pbid=%s&ec=%s" % (pbid, ec)

                video = Video(
                    title = response.meta['link_text'],
                    link = link,
                    athlete = athlete
                )

                try:
                    Video.objects.get(title=video.title)
                except ObjectDoesNotExist:
                    video.save()