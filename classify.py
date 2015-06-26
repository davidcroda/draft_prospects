import os
import django
import nltk
import pickle
import pprint

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "draft_prospects.settings")

django.setup()

from website.models import *
import code

def article_features(article):

    print "nltk.word_tokenize %s" % article.title
    tokens = nltk.word_tokenize(article.plain_text.encode('utf8'))
    print "nltk.Text %s" % article.title
    text = nltk.Text(tokens)
    print "nltk.FreqDist %s" % article.title
    frequency = nltk.FreqDist(text)
    print "nltk.pos_tag %s" % article.title
    pos = nltk.pos_tag(text)
    print "Count pronouns %s" % article.title

    nouns = [p[0] for p in pos if p[1][:3] == 'NNP']

    pprint.pprint(nouns)

    val = {}
    for noun in nouns:
        print "frequency.get %s" % noun
        val[noun] = frequency.get(noun)
        print " = %s" % val[noun]

    return val

articles = Entity.objects.exclude(plain_text='')[:100]

count = len(articles)

labeled_articles = ([
    (article_features(article), article.athlete.name) for article in articles
])

train_set, test_set = labeled_articles[count/2:], labeled_articles[:count/2]

if os.path.isfile('classifier.pickle'):
    print "Loading saved classifier"
    f = open('classifier.pickle')
    classifier = pickle.load(f)
    f.close()
else:
    classifier = nltk.NaiveBayesClassifier

print "Training..."

classifier.train(train_set)

f = open('classifier.pickle', 'wb')
pickle.dump(classifier, f)
f.close()

code.interact(local=locals())