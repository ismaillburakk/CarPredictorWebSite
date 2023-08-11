from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def homepage(request):
    return render(request, 'homepage.html')

def login_page(request):
    if request.method=='POST':
        username=request.POST.get("username")
        password=request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("priceForm:form")
        else:
            return render(request,  'home/login.html',{
                "error": "Username or password is wrong"
            })    
    return render(request, 'home/login.html')

def signup_page(request):
    if request.method=='POST':
        username = request.POST.get("username")
        email = request.POST.get("email")
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        password = request.POST.get("password")
        repassword = request.POST.get("repassword")
        
        if password== repassword:
            if User.objects.filter(username=username).exists():
                return render(request, "home/signup.html", 
                    {
                        "error": "Username is already token!!!!",
                        "username":username,
                        "email":email,
                        "firstname": firstname,
                        "lastname":lastname
                    })
            else:
                if User.objects.filter(email=email).exists():
                    return render(request, "home/signup.html", 
                    {
                        "error": "E-mail is already token!!!!",
                        "username":username,
                        "email":email,
                        "firstname": firstname,
                        "lastname":lastname
                    })
                else:
                    user = User.objects.create_user(username=username, email=email, first_name=firstname, last_name=lastname, password=password)
                    user.save()
                    return redirect("login")

        else:
            return render(request, "home/signup.html", 
            {
                "error": "Password doesn't match!!!!",
                "username":username,
                "email":email,
                "firstname": firstname,
                "lastname":lastname
            })
        
    return render(request, 'home/signup.html')
def LogOut(request):
    logout(request)
    return redirect("homepage")
