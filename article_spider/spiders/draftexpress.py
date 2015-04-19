# -*- coding: utf-8 -*-
import re

import django
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor

from article_spider.items import VideoItem
from website.models import Athlete


class DraftExpressSpider(CrawlSpider):

    name = "draftexpress"
    allowed_domains = ["draftexpress.com"]
    start_urls = (
        'http://www.draftexpress.com/videos/Scouting/',
    )

    rules = (
        Rule(LxmlLinkExtractor(allow='/video/[0-9]+'), callback='parse_video', follow=True),
    )

    athletes = ()

    def __init__(self):
        super(DraftExpressSpider, self).__init__()
        self.athletes = Athlete.objects.all()
        django.setup()
        assert len(self.athletes) > 0

    def parse_video(self, response):

        title = response.xpath('//td/b/text()').extract()[0]

        for athlete in self.athletes:

            if re.search(athlete.name, title, re.IGNORECASE):

                pb_id = re.search(r'player.ooyala.com\/v[0-9]+\/([a-z0-9]{32}?)"', response.body)
                youtube = re.search(r'youtube.com\/embed\/(.*?)"', response.body)
                embed = response.url

                if pb_id is not None:
                    pb_id = pb_id.group(1)
                    ec = re.search(r'\{cId: "([^"]*?)"',response.body).group(1)
                    embed = "http://player.ooyala.com/iframe.html#pbid=%s&ec=%s" % (pb_id, ec)
                elif youtube is not None:
                    youtube_id = youtube.group(1)
                    embed = "https://www.youtube.com/embed/%s" % youtube_id

                video = VideoItem(
                    title=title,
                    url=response.url,
                    embed=embed,
                    athlete=athlete
                )

                self.log("Processing Video for %s" % athlete.name)

                yield video