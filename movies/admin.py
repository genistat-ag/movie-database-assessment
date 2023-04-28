from django.contrib import admin
from .models import Movie, Rating, Report


class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'genre', 'year', 'creator','hidden', 'avg_rating', 'created_at', 'updated_at')


admin.site.register(Movie, MovieAdmin)
admin.site.register(Rating)
admin.site.register(Report)
