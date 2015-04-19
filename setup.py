#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='DraftProspects',
      version='0.1',
      description='Draft prospect information tracker',
      author='Dave Roda',
      author_email='davidcroda@gmail.com',
      url='https://bitbucket.org/davidcroda/draft_prospects',
      packages=find_packages(),
      install_requires=[
          'django',
          'django-model-utils',
          'html2text',
          'scrapy',
          'beautifulsoup4',
          'requests',
          'parsedatetime',
      ]

)