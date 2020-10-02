from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import *
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

# Create your views here.


def home(request):
    return render(request, './globalCert/index.html')


def signup(request):
    if request.method=='POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']


        if(len(username)>10):
            messages.error(request, "Username length must be less than 10 character.")
            return redirect('home')

        if not username.isalnum():
            messages.error(request, "Username should only contain character and numbers.")
            return redirect('home')

        if(pass1!=pass2):
            messages.error(request, "Password did not match. Please try again")
            return redirect('home')

        myuser = User.objects.create_user(username,email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request,"You have successfully registered. Welcome!")
        return redirect('home')
    else:
        return render(request,'./globalCert/signup.html')


def signin(request):
    if request.method=='POST':
        loginemail = request.POST['loginemail']
        loginpassword = request.POST['loginpass']
        user = authenticate(email = loginemail, password = loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In. Welcome!")
            return redirect('home')
        else:
            messages.error(request, "Invalid Credentials. Please try again")
            return redirect('home')
    return render(request, './globalCert/signin.html')

def forgotPassword(request):
    return render(request, './globalCert/forgotPassword.html')

def contact(request):
    if (request.method == 'POST'):
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        contact = Contact(name=name, email=email, subject=subject, message=message)
        contact.save()
    return render(request, './globalCert/index.html')

