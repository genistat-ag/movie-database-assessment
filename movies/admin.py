from django.contrib import admin
from .models import Movie, Rating, Report


class MovieAdmin(admin.ModelAdmin):
    list_display = ['id','genre','creator','year','avg_rating', 'created_at', 'updated_at']

    class Meta:
        model = Movie


admin.site.register(Movie, MovieAdmin)


class RatingAdmin(admin.ModelAdmin):
    list_display = ['id','movie','reviewer','score','created_at', 'updated_at']

    class Meta:
        model = Rating


admin.site.register(Rating, RatingAdmin)


class ReportAdmin(admin.ModelAdmin):
    list_display = ['id','movie','reporter','status','created_at', 'updated_at']

    class Meta:
        model = Report


admin.site.register(Report, ReportAdmin)

