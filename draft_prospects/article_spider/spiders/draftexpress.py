# -*- coding: utf-8 -*-
import re
import datetime

import django
from parsedatetime import parsedatetime
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.utils.response import get_base_url

from article_spider.items import VideoItem, ArticleItem
from website.models import Athlete


class DraftExpressSpider(CrawlSpider):

    name = "draftexpress"
    allowed_domains = ["draftexpress.com"]
    start_urls = (
        'http://www.draftexpress.com/archives/type/ncaa-draft-prospects/',
        'http://www.draftexpress.com/archives/type/all/',
        'http://www.draftexpress.com/videos/',
        'http://www.draftexpress.com/'

    )

    calendar = parsedatetime.Calendar()

    rules = (
        Rule(LxmlLinkExtractor(allow='/(archives|videos|profiles)'), follow=True),
        Rule(LxmlLinkExtractor(allow='/article'), callback='parse_article', follow=True),
        Rule(LxmlLinkExtractor(allow='/video/[0-9]+'), callback='parse_video', follow=True),
    )

    def __init__(self):
        super(DraftExpressSpider, self).__init__()
        self.athletes = Athlete.objects.all()
        django.setup()
        assert len(self.athletes) > 0

    def parse_video(self, response):

        title = response.xpath('//td/b/text()').extract()[0]

        pb_id = re.search(r'player.ooyala.com\/v[0-9]+\/([a-z0-9]{32}?)"', response.body)
        youtube = re.search(r'youtube.com\/embed\/(.*?)"', response.body)
        complex_player = re.search(r'player.complex.com\/tv\/js\/embed.js?cId=(.*?)&', response.body)
        embed = response.url

        if pb_id is not None:
            pb_id = pb_id.group(1)
            ec = re.search(r'\{cId: "([^"]*?)"',response.body).group(1)
            embed = "http://player.ooyala.com/iframe.html#pbid=%s&ec=%s" % (pb_id, ec)
        elif youtube is not None:
            youtube_id = youtube.group(1)
            embed = "https://www.youtube.com/embed/%s" % youtube_id
        elif complex_player is not None:
            cid = complex_player.group(1)
            embed = "http://player.complex.com/tv/iframe?cId=%s" % cid
            title = response.css('.red_heading_large::text').extract()[0]

        video = VideoItem(
            title=title,
            url=response.url,
            embed=embed
        )

        yield video

    def parse_article(self, response, **kwargs):

        # Some articles are really videos
        if response.body.find('player.complex.com') != -1:

            self.parse_video(response)
        else:

            relevance = kwargs.get('base_relevance', 0)

            base_tr = response.xpath('//tr[descendant::span[@class="red_heading_large"]]')
            title = base_tr.css('.red_heading_large::text')
            byline, date = base_tr.xpath('./following-sibling::tr//b/text()')[:2]
            content = base_tr.xpath('./following-sibling::tr/td/font/text()')

            images = content.xpath("//img/@src").extract()
            base = get_base_url(response)

            # Fri, 07/27/2012 - 4:16pm
            parsed = self.calendar.parse(date.extract()[0])
            date = datetime.datetime(*parsed[0][:7])
            main_content = "".join(content.extract())

            #replace relative image links
            for link in images:
                if link[0] == '/':
                    main_content.replace(link, base + link)

            yield ArticleItem(
                title=title.extract()[0],
                date=date,
                content=main_content,
                relevance=relevance,
                url=response.url
            )