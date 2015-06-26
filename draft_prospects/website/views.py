import pprint

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from website.models import Athlete, Entity


def index(request):

    filters = {}
    if 'athlete_id' in request.GET:
        filters['athlete_id'] = request.GET['athlete_id']

    if len(filters) > 0:
        athletes = Athlete.objects.filter(filters).order_by('draft_express_rank')
    else:
        athletes = Athlete.objects.all().order_by('draft_express_rank')
    paginator = Paginator(athletes, 25)
    page = request.GET.get('page', 1)

    try:
        athletes = paginator.page(page)
    except PageNotAnInteger:
        athletes = paginator.page(1)
    except EmptyPage:
        athletes = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {'athletes': athletes, 'page_range': paginator.page_range})


def view_entities(request, athlete_id):

    athlete = get_object_or_404(Athlete, id=athlete_id)

    filters = {
        'athlete_id': athlete_id
    }

    if request.GET.has_key('type'):
        filters['type'] = request.GET.get('type')

    entities = Entity.objects.filter(**filters).order_by('-date', '-relevance')

    return render(request, 'entities.html', {'athlete': athlete, 'entities': entities})


def view_entity(request, entity_id):
    entity = get_object_or_404(Entity, id=entity_id)
    # entity.embed = entity.embed.replace(".html", ".js")
    template = "entities/%s.html" % entity.type
    return render(request,template, {'entity': entity})