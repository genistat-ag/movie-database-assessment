from django.contrib import admin

from .models import Movie, Rating, Report

admin.site.register(Movie)
admin.site.register(Rating)  # bug: model missing from admin site
admin.site.register(Report)  # bug: model missing from admin site
