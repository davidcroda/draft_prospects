from django.contrib import admin

from .models import Athlete, Entity


# Register your models here.

class EntityAdmin(admin.ModelAdmin):
    list_display = ['title', 'athlete', 'relevance', 'type']
    list_filter = ['athlete', 'relevance', 'type']


admin.site.register(Athlete)
admin.site.register(Entity, EntityAdmin)