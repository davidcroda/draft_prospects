import re
import logging

from bs4 import BeautifulSoup
import requests
import django
from django.core.exceptions import ObjectDoesNotExist

from models import Athlete


class ProspectScraper:

    url = "http://www.draftexpress.com/rankings/Top-100-Prospects/%s/"

    log = logging.getLogger('django')
    log.setLevel('DEBUG')

    def __init__(self):
        django.setup()

    def scrape(self):

        for page in range(1,5):

            resp = requests.get(self.url % page)

            if resp.status_code == 200:

                soup = BeautifulSoup(resp.text)

                players = soup.select('a b')

                for player in players:

                    athlete = self.parse_player(player)

                    try:
                        existing = Athlete.objects.get(first_name=athlete.first_name, last_name=athlete.last_name)
                        athlete.id = existing.id
                        self.log.info('Existing athlete found %s' % existing.name)
                    except ObjectDoesNotExist:
                        self.log.info('Athlete not found, creating')
                    athlete.save()

            else:
                self.log.error("Received status %s for url: %s" % (resp.status_code, self.url % page))

    def parse_player(self, player):

        self.log.info(player)

        first_name, last_name = player.text.split(" ")

        for p in player.parents:
            if p.name == "td":
                parent = p
                break

        matches = re.search(r"\((.+?) - (.+?)\)", parent.text)

        school = matches.group(1).strip()
        year = matches.group(2).strip()

        matches = re.search(r"([0-9.]+) years old", parent.text)

        age = matches.group(1).strip()

        matches = re.search(r"(([0-9])+'([0-9])+\")", parent.text)

        height = matches.group(1).strip()

        height_inches = (int(matches.group(2)) * 12) + int(matches.group(3))

        matches = re.search(r"([0-9]+) lbs", parent.text)

        weight = matches.group(1)

        rank = parent.previous_sibling.previous_sibling.previous_sibling.previous_sibling.text.strip(". ")

        self.log.info("Rank: %s, First Name: %s, Last Name: %s, School: %s, Year: %s, Age: %s, Height: %s, Weight: %s" % (rank, first_name, last_name, school, year, age, height, weight))

        return Athlete(first_name=first_name,
                       last_name=last_name,
                       school=school,
                       year=year,
                       age=age,
                       height=height,
                       height_inches=height_inches,
                       weight=weight,
                       draft_express_rank=rank)

if __name__ == "__main__":
    scraper = ProspectScraper()
    scraper.scrape()

