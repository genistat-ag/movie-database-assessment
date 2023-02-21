from django.contrib import admin
from .models import Movie, Rating, Report

#Registering required models
admin.site.register(Movie)
admin.site.register(Rating)
admin.site.register(Report)
