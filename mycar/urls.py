
from django.contrib import admin 
from django.urls import path
from mycar import views

urlpatterns = [
    path('',views.home,name='home'),
    path('signup/',views.signup ,name='signup'),
    path('register/',views.register ,name='register'),
    path('otp/',views.otp ,name='otp'),
    path('login/',views.login ,name='login'),
    path('logout/',views.logout ,name='logout'),
    path('changepass/',views.changepass ,name='changepass'),
    path('forgot/',views.forgot ,name='forgot'),
    path('profile/',views.profile,name='profile'),
    path('pricing/',views.pricing,name='pricing'),
    path('contact/',views.contact,name='contact'),
    path('rent-car/',views.rent_car,name='rent-car'),
    path('dash/',views.dash,name='dash'),
    path('summary/<int:pk>',views.summary,name='summary'),
    path('summary/paymenthandler/<int:pk>', views.paymenthandler, name='paymenthandler'),


]
