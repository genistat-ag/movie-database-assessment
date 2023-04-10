from django.urls import path
from mainapp.views import *

app_name = "main"

urlpatterns = [
    #API urls    
    
    #rendering urls
    path('', login, name="login"),
    path('registration', registration, name="registration"),
    path('dashboard', dashboard, name="dashboard"),
    path('logout/', logout, name="logout"),
    path('movies/', movies, name="movies"),
    path('ratings/', ratings, name="ratings"),
    path('reports/', reports, name="reports"),
]