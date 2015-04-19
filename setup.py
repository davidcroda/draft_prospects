#!/usr/bin/env python

from distutils.core import setup

setup(name='DraftProspects',
      version='0.1',
      description='Draft prospect information tracker',
      author='Dave Roda',
      author_email='davidcroda@gmail.com',
      url='https://bitbucket.org/davidcroda/draft_prospects',
      packages=['draft_prospects','article_spider','website'],
      install_requires=[
          'django',
          'html2text',
          'scrapy',
          'beautifulsoup4',
          'requests'
      ])