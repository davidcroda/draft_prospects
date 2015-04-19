from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^entities/([0-9]*)/?$', views.view_entities, name='view-entities'),
    url(r'^entity/([0-9]*)/?$', views.view_entity, name='view-entity')
]