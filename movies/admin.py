from django.contrib import admin
from .models import Movie,Rating,Report


class MovieAdmin(admin.ModelAdmin):
    actions = ['inappropriate', 'rejected']

    def make_inappropriate(self, request, queryset):
        queryset.update(status='Inappropriate')
        for data in queryset:
            Movie.objects.filter(id=data.id).update(deleted=False)

    make_inappropriate.short_description = "Inappropriate"

    def make_rejected(self, request, queryset):
        queryset.update(status='Rejected')
        for data in queryset:
            Movie.objects.filter(id=data.id).update(visibility=True)

    make_rejected.short_description = "Rejected"


admin.site.register(Movie, MovieAdmin)
admin.site.register(Rating)
admin.site.register(Report)
