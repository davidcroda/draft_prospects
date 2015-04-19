# -*- coding: utf-8 -*-
import datetime

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.utils.response import get_base_url
import parsedatetime

from article_spider.items import ArticleItem


class NbadraftSpider(CrawlSpider):

    name = "nbadraftnet"
    allowed_domains = ["nbadraft.net"]
    start_urls = (
        'http://www.nbadraft.net/articles',
    )

    calendar = parsedatetime.Calendar()

    rules = (
        Rule(LxmlLinkExtractor(restrict_xpaths="//div[@id='content']//td/a"), callback='parse_article'),
        Rule(LxmlLinkExtractor(allow='/articles')),
        Rule(LxmlLinkExtractor(allow='/players/'), callback='parse_article', cb_kwargs={'base_relevance': 100})
    )

    def parse_article(self, response, **kwargs):

        relevance = kwargs.get('base_relevance',0)

        content_selector = response.css('#content-area .content')
        images = content_selector.xpath("//img/@src").extract()
        base = get_base_url(response)

        #Fri, 07/27/2012 - 4:16pm
        parsed = self.calendar.parse(response.css('.date::text').extract()[0])
        date = datetime.datetime(*parsed[0][:7])
        main_content = content_selector.extract()[0]

        #replace relative image links
        for link in images:
            if link[0] == '/':
                main_content.replace(link,base + link)

        title = response.xpath('//h1/text()').extract()[0]

        yield ArticleItem(
            title=title,
            date=date,
            content=main_content,
            relevance=relevance,
            url=response.url
        )