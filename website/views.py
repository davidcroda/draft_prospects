from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from website.models import Athlete, Article


def index(request):

    filters = {}
    if 'athlete_id' in request.GET:
        filters['athlete_id'] = request.GET['athlete_id']

    if len(filters) > 0:
        articles = Article.objects.filter(filters)
    else:
        articles = Article.objects.all()
    paginator = Paginator(articles, 100)
    page = request.GET.get('page', 1)

    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {'articles': articles, 'page_range': paginator.page_range})
