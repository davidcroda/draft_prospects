# -*- coding: utf-8 -*-

import sys
import os

BOT_NAME = 'article_spider'

SPIDER_MODULES = ['article_spider.spiders']
NEWSPIDER_MODULE = 'article_spider.spiders'

ITEM_PIPELINES = {
    'article_spider.pipelines.SaveArticlePipeline': 100
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'article_spider (+http://www.yourdomain.com)'

sys.path.append('/Users/dave/src/draft_prospects')

os.environ['DJANGO_SETTINGS_MODULE'] = 'draft_prospects.settings'

LOG_LEVEL = 'INFO'