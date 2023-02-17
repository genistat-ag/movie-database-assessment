from django.contrib import admin
from .models import Movie, Rating, Report

admin.site.register(Rating)
admin.site.register(Report)

class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'genre', 'year', 'created_at', 'updated_at', 'creator', 'avg_rating',)

admin.site.register(Movie, MovieAdmin)