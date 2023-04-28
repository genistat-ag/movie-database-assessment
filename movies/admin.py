from django.contrib import admin
from .models import Movie, Rating, Report


class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'genre', 'year', 'creator', 'hidden', 'avg_rating', 'created_at', 'updated_at')


admin.site.register(Movie, MovieAdmin)


class RatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'movie', 'score','reviewer', )


admin.site.register(Rating, RatingAdmin)
admin.site.register(Report)
