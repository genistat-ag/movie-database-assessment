from django.contrib import admin
from .models import Movie,Rating,Report

def make_inappropriate(modeladmin, request, queryset):
    queryset.update(state='Mark movie as inappropriate')
    for data in queryset:
        Movie.objects.filter(id=data.id).update(visibility=False)
make_inappropriate.short_description = "Mark as Inappropriate"

def make_rejected(modeladmin, request, queryset):
    queryset.update(state='Mark as Rejected')
make_rejected.short_description = "Mark as Rejected"

class ReportAdminView(admin.ModelAdmin):
    actions = [make_inappropriate, make_rejected]


admin.site.register(Movie)
admin.site.register(Rating)
admin.site.register(Report,ReportAdminView)
