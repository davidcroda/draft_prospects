from bs4 import BeautifulSoup
import requests, re, logging
from models import Athlete
import django
from django.core.exceptions import ObjectDoesNotExist

class ProspectScraper:

    url = "http://www.draftexpress.com/rankings/Top-100-Prospects/%s/"

    log = logging.getLogger('django')
    #log.setLevel('DEBUG')

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
                        existing = Athlete.objects.get(name=athlete.name)
                        athlete.id = existing.id
                        self.log.info('Existing athlete found %s' % existing.name)
                    except ObjectDoesNotExist:
                        self.log.info('Athlete not found, creating')
                        pass
                    athlete.save()

            else:
                self.log.error("Received status %s for url: %s" % (resp.status_code, self.url % page))

    def parse_player(self, player):

        self.log.info(player)

        name = player.text

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

        self.log.info("Rank: %s, Name: %s, School: %s, Year: %s, Age: %s, Height: %s, Weight: %s" % (rank, name, school, year, age, height, weight))

        return Athlete(name=name,
                       school=school,
                       year=year,
                       age=age,
                       height=height,
                       height_inches = height_inches,
                       weight=weight,
                       draft_express_rank = rank)

if __name__ == "__main__":
    scraper = ProspectScraper()
    scraper.scrape()

