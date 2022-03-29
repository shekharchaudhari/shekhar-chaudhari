from tempfile import tempdir
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import *
from django.conf import settings
from django.core.mail import send_mail
from random import randrange

# Create your views here.

def home(request):
  
    return render(request,'index.html')
    
def signup(request):
  
    return render(request,'login_signup.html')

def register(request):
    if request.method == "POST":
        try:
            User.objects.get(email=request.POST['email'])
            msg = 'Email is already register'
            return render(request,'login_signup.html',{'msg':msg})
        except:
            if request.POST['password'] == request.POST['cpass']:
                global temp
                temp = {
                    'uname':request.POST['uname'],
                    'email':request.POST['email'],
                    'password':request.POST['password'],
                    'mobile':request.POST['mobile'],
                }
               
                otp = randrange(1000,9999)

                subject = 'welcome to car pooling'
                message = f'Welcome to App {otp}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [request.POST['email'], ]
                send_mail( subject, message, email_from, recipient_list )
                return render(request,'otp.html',{'otp':otp})

            else:
                return render(request,'login_signup.html',{'msg':'Both passwords are not same'})

    return render(request,'login_signup.html') 

def otp(request):
    if request.method == "POST":
        if request.POST['otp'] == request.POST['uotp']:
            global temp
            User.objects.create(
                uname = temp['uname'],
                email = temp['email'],
                password = temp['password'],
                mobile = temp['mobile'],
            )
            return render(request,'login_signup.html',{'msg':'Account Created'})
        return render(request,'otp.html',{'msg':'Invalid OTP','otp':request.POST['otp']})
    return render(request,'login_signup.html')

def login(request):
    try: 
        uid = User.objects.get(email=request.session['email'])
        return render(request,'dashboard1.html',{'uid':uid})
    except:    
        if request.method == "POST":
            try:
                uid = User.objects.get(email=request.POST['email'])
                if request.POST['password'] == uid.password:
                    request.session['email'] = request.POST['email']
                    return render(request,'dashboard1.html',{'uid':uid})
                return render(request, 'login_signup.html',{'msg':'invalid password','uid':uid})
            except:
                return render(request, 'login_signup.html',{'msg':'email not registered!!','uid':uid})
        return render(request,'login_signup.html')

   
def logout(request):
    del request.session['email']
    return render(request,'login_signup.html')

def changepass(request):
    uid = User.objects.get(email=request.session['email'])
    if request.method == "POST":
        if request.POST['password'] == request.POST['cpassword']:
            uid.password = request.POST['password']
            uid.save()
            return render(request,'changepass.html',{'msg':'password changed sucessfully.','uid':uid})
        return render(request,'changepass.html',{'msg':'password does not match.','uid':uid})    
    return render(request,'changepass.html',{'uid':uid})
        
def forgot(request):  
    if request.method == "POST":
        try:  
            uid = User.objects.get(email=request.POST['email'])
            if request.POST['email'] == uid.email:
                yourpass = uid.password
                subject = 'welcome to car pooling'
                message = f'your password: {yourpass}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [request.POST['email'], ]
                send_mail( subject, message, email_from, recipient_list )
                return render(request,'forgot.html',{'msg':'password sent successfully.'})
        except:        
            return render(request,'forgot.html',{'msg':'invalid email'})    
    return render(request,'forgot.html')        


def profile(request):
    uid = User.objects.get(email=request.session['email'])
    if request.method == "POST":
        uid.uname = request.POST['uname']
        uid.email = request.POST['email']
        uid.mobile = request.POST['mobile']
        uid.address = request.POST['address']
        if 'pic' in request.FILES:
            uid.pic = request.FILES['pic']
        uid.save()    
        return render(request,'profile.html',{'uid':uid,'msg':'Profile has been updated'})
    return render(request,'profile.html',{'uid':uid})