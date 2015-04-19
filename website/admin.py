from django.contrib import admin
from .models import Athlete, Article

# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title','athlete','relevance']
    list_filter = ['athlete','relevance']


admin.site.register(Athlete)
admin.site.register(Article, ArticleAdmin)