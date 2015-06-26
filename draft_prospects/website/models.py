from datetime import datetime
import hashlib
from django.db import models


class Athlete(models.Model):

    def __unicode__(self):
        return self.name

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    school = models.CharField(max_length=255)
    year = models.CharField(max_length=255)
    age = models.FloatField()
    height = models.CharField(max_length=10)
    height_inches = models.IntegerField()
    weight = models.IntegerField()
    draft_express_rank = models.IntegerField()

    @property
    def name(self):
        return ''.join([self.first_name, ' ', self.last_name])


class Entity(models.Model):
    """
    I really wanted to do this with Single Table Inheritance, but it doesn't
    seem possible in Django. So I had to hack this together. I am sure with more
    time and/or python / django experience this could be done with inheritance
    """

    title = models.CharField(max_length=255)
    url = models.TextField()
    date = models.DateTimeField(default=datetime.now)
    relevance = models.IntegerField(default=0)
    athlete = models.ForeignKey(Athlete)
    hash = models.CharField(max_length=64)

    ARTICLE = 'AR'
    VIDEO = 'VI'
    QUOTE = 'QU'

    TYPE_CHOICES = (
        (ARTICLE, 'Article'),
        (VIDEO, 'Video'),
        (QUOTE, 'quote'),
    )

    type = models.CharField(max_length=2, choices=TYPE_CHOICES, default=ARTICLE)

    #Article
    content = models.TextField()
    plain_text = models.TextField()
    modified = models.DateField(auto_now=True)

    #Video
    embed = models.CharField(max_length=500)

    #Quote
    from_name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.title

    def get_hash(self):
        digest = hashlib.md5()

        if self.type in ['article', 'quote']:
            digest.update(self.plain_text)
        else:
            digest.update(self.url)

        self.hash = digest.hexdigest()
        return self.hash