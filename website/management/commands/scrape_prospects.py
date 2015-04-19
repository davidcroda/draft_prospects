from django.core.management.base import BaseCommand, CommandError

from website.scraper import ProspectScraper


class Command(BaseCommand):

    help = 'Scrape top 100 prospects from DraftExpress.com'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):

        scraper = ProspectScraper()

        try:
            scraper.scrape()
        except Exception as e:
            raise CommandError("%s" % e.message)
