from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout

# Create your views here.

def login_view(request):
    if request.method=="POST":
        form=AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            login(request,form.get_user())
            return redirect("products:list")

    else:
        form=AuthenticationForm()

    return render(request,"Account/login.html",{"form":form})   



def logout_view(request):
    logout(request)
    return redirect("products:list")

