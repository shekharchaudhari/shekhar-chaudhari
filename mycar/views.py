from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import *
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

from django.conf import settings
from django.core.mail import send_mail
from random import randrange

# Create your views here.

def home(request):
    cars = Car.objects.all()
    return render(request,'index.html',{'cars':cars})
    
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
        return render(request,'dashboard.html',{'uid':uid})
    except:    
        if request.method == "POST":
            try:
                uid = User.objects.get(email=request.POST['email'])
                if request.POST['password'] == uid.password:
                    request.session['email'] = request.POST['email']
                    return render(request,'dashboard.html',{'uid':uid})
                return render(request, 'login_signup.html',{'msg':'invalid password','uid':uid})
            except:
                return render(request, 'login_signup.html',{'msg':'email not registered!!','uid':uid})
        return render(request,'login_signup.html')

   
def logout(request):
    try:
        uid = User.objects.get(email=request.session['email'])
        del request.session['email']
        return render(request,'login_signup.html')
    except:
        return render(request,'index.html')

            

def changepass(request):
    uid = User.objects.get(email=request.session['email'])
    if request.method == "POST":
        if request.POST['opassword'] == uid.password:
            if request.POST['password'] == request.POST['cpassword']:
                uid.password = request.POST['password']
                uid.save()
                return render(request,'changepass.html',{'msg':'password changed sucessfully.','uid':uid})
            return render(request,'changepass.html',{'msg':'password does not match.','uid':uid})
        return render(request,'changepass.html',{'msg':'Old Password is incorrect','uid':uid})    
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

def pricing(request):
    return render(request,'pricing.html')   

def dash(request):
    uid = User.objects.get(email=request.session['email'])
    return render(request,'dashboard.html',{'uid':uid})      

def contact(request):
    uid = User.objects.get(email=request.session['email'])
    return render(request,'contact.html',{'uid':uid})

def rent_car(request):
    try:    
        uid = User.objects.get(email=request.session['email'])
        cars = Car.objects.all()
        if request.method == "POST":
            Trip.objects.create(
                users = uid,
                pick_loc = request.POST['pick_loc'],
                drop_loc = request.POST['drop_loc'],
                p_date = request.POST['p_date'],
                d_date = request.POST['d_date'],
                pick_time = request.POST['pick_time'],
                )
            return render(request,'cars.html',{'uid':uid, 'cars':cars}) 
        return render(request,'dashboard.html',{'uid':uid})       
    except: 
        return render(request,'login_signup.html')

razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

def summary(request,pk):
    uid = User.objects.get(email=request.session['email'])
    cars = Car.objects.get(id=pk)
    trip = Trip.objects.filter(users=uid)[::-1][0]
    book = Book.objects.create(
        user = uid,
        car = cars,
        trip = trip,
        amount = cars.p_hour
    )
    currency = 'INR'
    amount = cars.p_hour*100  # Rs. 200
 
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
 
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = f'paymenthandler/{book.id}'
 
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    context['cars'] = cars
    context['uid'] = uid
    context['trip'] = trip
    return render(request,'summary.html',context)


@csrf_exempt
def paymenthandler(request,pk):
 
    # only accept POST request.
    if request.method == "POST":
        try:
            book = Book.objects.get(id=pk)
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            amount = book.amount*100  # Rs. 200
            try:

                # capture the payemt
                razorpay_client.payment.capture(payment_id, amount)
                book.pay_id = payment_id
                book.verify = True
                book.save()
                # render success page on successful caputre of payment
                return render(request, 'success.html')
            except:

                # if there is an error while capturing payment.
                return render(request, 'fail.html')
           
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()

