from django.contrib import admin
from .models import Movie, Report, Rating

admin.site.register(Movie)
admin.site.register(Report)
admin.site.register(Rating)