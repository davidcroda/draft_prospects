import os
import sys
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from article_spider.spiders.draftexpress import DraftExpressSpider
from article_spider.spiders.nbadraft import NbadraftSpider
from scrapy.utils.project import get_project_settings
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):

    help = 'Run crawlers'

    def __init__(self):
        BaseCommand.__init__(self)

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):

        spiders = [DraftExpressSpider(), NbadraftSpider()]
        settings = get_project_settings()

        for spider in spiders:
            crawler = Crawler(settings)
            crawler.signals.connect(self.stop, signal=signals.spider_closed)
            crawler.configure()
            crawler.crawl(spider)
            print "Starting Spider [%s]" % spider.name
            crawler.start()

        log.start(loglevel=settings.get('LOG_LEVEL'))
        reactor.run()

    def stop(self):
        print "Stopping Reactor"
        reactor.stop()
        sys.exit(0)