from django.shortcuts import render, redirect
from . import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


# Create your views here.

def register(request):
    error = ""
    if request.method == "POST":
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account created successfully!")
            return redirect("login")
        error = list(form.errors.items())
        for i in range(len(error)):
            error[i] = "".join(error[i][1])
    else:
        form = forms.RegistrationForm()
    if error != "":
        print("ERROR::::: " + str(error))
    return render(request, 'Users/register.html', {"errors": error})


def logoutPage(request):
    logout(request)
    return render(request, "Users/logout.html")


def loginPage(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("main_home")
        else:
            return render(request, "Users/login.html", {"error": "Username or password is incorrect"})
    else:
        return render(request, "Users/login.html")
