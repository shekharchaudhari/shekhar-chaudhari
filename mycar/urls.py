
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
]
