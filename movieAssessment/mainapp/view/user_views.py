from mainapp.views import *

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = Users.objects.filter(Q(email = username)|Q(username = username))
            if user:
                user = user.filter(password=password).first()
                if user:
                    request.session["email"] = user.email
                    request.session["mobile"] = user.mobile
                    request.session["full_name"] = user.full_name
                    request.session["last_name"] = user.last_name
                    request.session["id"] = user.id
                    request.session["user_pic"] = str(user.user_pic) if user.user_pic else ""
                    messages.success(request,"Login Successful")
                    return redirect(reverse("main:dashboard"))
                else:
                    messages.warning(request,"Incorrect Password for "+username+"!")
            else:
                messages.warning(request,"Incorrect Username("+username+")!")
        context = {
            "username":username
        }
    else: context = {}
    return render(request, 'login.html',context)

@login_check
def logout(request):
    try:
        for s in Session.objects.all().order_by("-expire_date"):  # delete session data
            if 'id' in s.get_decoded() and request.session.get('id') == s.get_decoded()["id"]:
                Session.objects.filter(session_key=s.session_key).delete()
                break
        messages.success(request, "Logout Successful.")
        return redirect("/")
    except:    
        messages.success(request, "Logout Successful.")
        return redirect("/")
 
@login_check   
def dashboard(request):
    context = {}
    return render(request, 'dashboard.html',context)

