from django.contrib import admin
from .models import catagory,customer,Products,order,profile
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(catagory)
admin.site.register(customer)
admin.site.register(Products)
admin.site.register(order)
admin.site.register(profile)

#mix profile info and user info
class profileinline(admin.StackedInline):
    model=profile

#extend user model
class UserAdmin(admin.ModelAdmin):
    model=User
    # fields=['username','first_name','last_name','email','is_staff','is_superuser']
    
    inlines=[profileinline]

#un-register old way
admin.site.unregister(User)

#reregister new way
admin.site.register(User, UserAdmin)