from django.db import models

class Athlete(models.Model):

    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=255)
    school = models.CharField(max_length=255)
    year = models.CharField(max_length=255)
    age = models.FloatField()
    height = models.CharField(max_length=10)
    height_inches = models.IntegerField()
    weight = models.IntegerField()
    draft_express_rank = models.IntegerField()

class Video(models.Model):

    def __unicode__(self):
        return self.title

    title = models.CharField(max_length=255)
    url = models.CharField(max_length=500)
    athlete = models.ForeignKey(Athlete)

class Article(models.Model):

    def __unicode__(self):
        return self.link_text

    title = models.CharField(max_length=255)
    link_text = models.CharField(max_length=255)
    url = models.CharField(max_length=500)
    content = models.TextField()
    summary = models.TextField()
    plain_text = models.TextField()
    relevance = models.IntegerField()
    athlete = models.ForeignKey(Athlete)
    hash = models.CharField(max_length=64)