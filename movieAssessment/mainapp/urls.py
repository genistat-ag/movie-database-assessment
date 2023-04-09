from django.urls import path
from mainapp.views import *

app_name = "main"

urlpatterns = [
    #API urls    
    
    #rendering urls
    path('', login, name="login"),
    path('dashboard', dashboard, name="dashboard"),
    path('logout/', logout, name="logout"),
]