# -*- coding: utf-8 -*-
import django
from django.core.exceptions import ObjectDoesNotExist
import html2text
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
import re
from site.models import Article, Athlete
from scrapy.shell import inspect_response
import hashlib

class NbadraftSpider(CrawlSpider):

    name = "nbadraftnet"
    allowed_domains = ["nbadraft.net"]
    start_urls = (
        'http://www.nbadraft.net/articles',
    )

    rules = (
        Rule(LxmlLinkExtractor(restrict_xpaths="//div[@id='content']//td/a"), callback='parse_article'),
        Rule(LxmlLinkExtractor(allow='/articles')),
        Rule(LxmlLinkExtractor(allow='/players/'), callback='parse_article', cb_kwargs={'base_relevance': 100})
    )

    athletes = ()

    LINK_MATCH_SCORE = 50
    FULL_MATCH_SCORE = 10
    LAST_MATCH_SCORE = 2
    MIN_RELEVANCE_LEVEL = 10

    def __init__(self):
        super(NbadraftSpider, self).__init__()
        self.athletes = Athlete.objects.all()
        django.setup()
        assert len(self.athletes) > 0

    def parse_article(self, response, **kwargs):

        base_relevance = kwargs.get('base_relevance',0)
        main_content = response.css('#content-area').extract()[0]
        title = response.xpath('//h1/text()').extract()[0]

        for athlete in self.athletes:

            last_name = athlete.name.split(' ')[1]

            full_matches = re.findall(athlete.name, response.body, re.IGNORECASE)
            last_matches = re.findall(last_name, response.body, re.IGNORECASE)

            relevance = int(base_relevance) + \
                (len(full_matches) * self.FULL_MATCH_SCORE) + \
                (len(last_matches) * self.LAST_MATCH_SCORE)

            if response.meta['link_text'].find(athlete.name) != -1 or title.find(athlete.name) != -1:
                relevance += self.LINK_MATCH_SCORE

            if relevance > self.MIN_RELEVANCE_LEVEL:

                self.log("Article: %s, Athlete: %s, Relevance: %s" %
                         (response.meta['link_text'], athlete.name, relevance))

                plain_text = html2text.html2text(main_content)

                digest = hashlib.md5()
                digest.update(plain_text.encode('utf-8'))

                article = Article(
                    title=title,
                    link_text=response.meta['link_text'],
                    url=response.url,
                    content=response.body,
                    summary=main_content,
                    plain_text=plain_text,
                    relevance=relevance,
                    athlete=athlete,
                    hash=digest.hexdigest()
                )

                try:
                    existing = Article.objects.get(url=response.url, athlete=athlete)

                    self.log('Existing article found for url: %s' % response.url)

                    if article.hash != existing.hash:

                        self.log('New Hash: %s != Existing Hash: %s, saving updated copy' % (article.hash, existing.hash))

                        article.id = existing.id
                        article.save()

                except ObjectDoesNotExist:

                    article.save()

