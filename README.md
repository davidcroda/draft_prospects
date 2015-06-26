# README #

Project to automatically scrape and parse information about the top 100 nba draft prospects

### Setup ###
* `$ virtualenv new venv`
* `$ source venv/bin/activate`
* `$ python setup.py install`
* update draft_prospects/settings.py
* `$ ./manage.py scrape_prospects` - imports the top 100 prospect names to seed the database

### Crawlers ###
* `$ scrapy crawl nbadraftnet` - Crawl articles on nbadraft.net
