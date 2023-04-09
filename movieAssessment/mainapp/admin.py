from django.contrib import admin
from mainapp.models import *

class UsersAdmin(admin.ModelAdmin):
    list_display  = ['first_name', 'last_name','username','email','mobile','created_at']
    search_fields = ['first_name', 'last_name','username','email','mobile']
admin.site.register(Users,UsersAdmin)
