from django.contrib import admin
from .models import *

# Register your models here.

# admin.site.register(User)

@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display = ['uname','password','email','mobile','address','pic']

admin.site.register(Trip)

admin.site.register(Car)

admin.site.register(Book)
