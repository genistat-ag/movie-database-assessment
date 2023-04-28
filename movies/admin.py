from django.contrib import admin
from .models import Movie, Rating


class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'genre', 'year', 'creator', 'avg_rating', 'created_at', 'updated_at')
admin.site.register(Movie,MovieAdmin)
admin.site.register(Rating)
