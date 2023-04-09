from django.shortcuts import redirect
from mainapp.models import Users
from django.contrib import messages

def login_check(function):
    def wrap(request, *args, **kwargs):
        if request.session.get('id'):
            return function(request, *args, **kwargs)
        else:
            messages.warning(request, "Please login first!")
            next_url = request.path
            return redirect("/?next="+next_url) #Login page url
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
