from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import *
import datetime
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .utils import token_generator
import threading
# from validate_email import validate_email
from django.core.mail import EmailMessage
from django.utils.encoding import *
from django.utils.http import *
from django.contrib.sites.shortcuts import *
from django.contrib.auth.tokens import PasswordResetTokenGenerator


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
            return render(request,'./globalCert/signup.html')

        if not username.isalnum():
            messages.error(request, "Username should only contain character and numbers.")
            return render(request,'./globalCert/signup.html')

        if(pass1!=pass2):
            messages.error(request, "Password did not match. Please try again")
            return render(request,'./globalCert/signup.html')

        myuser = User.objects.create_user(username,email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active= False
        myuser.save()
        uidb64 = urlsafe_base64_encode(force_bytes(myuser.pk))

        domain = get_current_site(request).domain
        link=reverse('activate',kwargs={'uidb64':uidb64, 'token':token_generator.make_token(myuser)})
        email_subject = "Activate Your Account"
        activate_url = 'http://'+domain+link
        email = EmailMessage(
            email_subject,
            'Hi '+myuser.username+' Welcome To Globalcert. Please verify your account using this link '+activate_url,
            'noreply@semicolon.com',
            [email],
        )
        email.send(fail_silently=False)
        messages.success(request,"You have successfully registered. Welcome!")
    return render(request,'./globalCert/signup.html')

class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            uid=force_text(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)
            print(user)
        except Exception as identifier:
            user=None
        if user is not None:
            user.is_active=True
            user.save()
            messages.success(request,"Account has been Activated")
            return render(request, './globalCert/signin.html')
        return redirect('signin')


def handleLogout(request):
    logout(request)
    # messages.success(
    #     request, "Successfully Logged Out. Visit after website again!. If you have any issue then post it on contact tab. Thankyou!")
    return redirect('home')

def signin(request):
    if request.method=='POST':
        username = request.POST['username']
        loginpassword = request.POST['loginpass']
        user = authenticate(username = username, password = loginpassword)
        if user is not None:
            login(request, user)
            # messages.success(request, "Successfully Logged In. Welcome!")
            return redirect('home')
        else:
            messages.error(request, "Invalid Credentials. Please try again")
            return render(request, './globalCert/signin.html')
    return render(request, './globalCert/signin.html')

def forgotPassword(request):
    if request.method=='POST':
        email=request.POST['email']
        print(email)
        if not validate_email(email):
            messages.error(request,'Please enter a valid email')
            return render(request, './globalCert/forgotPassword.html')
        user=User.objects.filter(email=email)
        if user.exists():
            domain = get_current_site(request).domain
            link=reverse('set-new-password',kwargs={'uidb64':uidb64, 'token':token_generator.make_token(myuser)})
            email_subject = "Reset Your password"
            reset_password_url = 'http://'+domain+link
            email = EmailMessage(
                email_subject,
                'Hi '+myuser.username+' Welcome To Globalcert. Please click this link to reset your password '+reset_password_url,
                'noreply@semicolon.com',
                [email],)
            email.send(fail_silently=False)
            messages.success(request,'we have sent you an email with instructions on how to reset your password')
    return render(request, './globalCert/forgotPassword.html')


def viewCert(request):
    return render(request, './globalCert/viewCert.html')

def contact(request):
    if (request.method == 'POST'):
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        if(len(subject)<5 or len(message)<10):
            messages.error(request, "Sorry your response is not submitted. Please enter valid details")
        else:
            contact = Contact(name=name, email=email, subject=subject, message=message)
            contact.save()
            messages.success(request, "Your response has been Submitted Successfully. Thank You!")
    return redirect('home')

class SetNewPasswordView(View):
    def get(self,request,uidb64,token):
        context={
            'uidb64':uidb64,
            'token':token

        }
        return render(request, './globalCert/forgotPassword.html')

    def post(self,request,uidb64,token):
        context={

            'uidb64':uidb64,
            'token':token,
            'has_error':False
        }

        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']


        if(len(username)>10):
            messages.error(request, "Username length must be less than 10 character.")
            context['has_error']=True
            return render(request,'./globalCert/signup.html')

        if(pass1!=pass2):
            messages.error(request, "Password did not match. Please try again")
            context['has_error']=True
            return render(request, './globalCert/set-new-password.html',context)
        try:    
            user_id=force_text(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            messages.success(request,'Password reset success')
            return redirect('login')
        except DjangoUnicodeDecodeError as identifier:
            messages.error(request,'Something went wrong')
        return render(request, './globalCert/set-new-password.html',context)

        