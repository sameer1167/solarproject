from django.db import models
from django.utils.timezone import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.


#create customer profile
class profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    date_modified=models.DateTimeField(User,auto_now=True)
    phone=models.CharField(max_length=20,blank=True)
    address_1= models.CharField(max_length=200,blank=True)
    address_2=models.CharField(max_length=20,blank=True)
    city=models.CharField(max_length=200,blank=True)
    state=models.CharField(max_length=200,blank=True)
    pin_code=models.CharField(max_length=200,blank=True)
    country=   models.CharField(max_length=200,blank=True)
    old_cart=models.CharField(max_length=200,blank=True,null=True)


    def __str__(self):
        return self.user.username                   #this is for admin section on backend
    

#create the user profile by default when the user sign up
def create_profile(sender,instance, created,**kwargs):
    if created:
        user_profile=profile(user=instance)                    
        user_profile.save()

#automate the profile things
post_save.connect(create_profile, sender=User) 


 

class catagory(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name

class customer(models.Model):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    Contact_number=models.CharField(max_length=100)
    Email=models.EmailField(max_length=100)
    Password=models.CharField(max_length=100)

    def __str__(self):
        return f'{self.first_name}.{self.last_name}'


        

class Products(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discription = models.TextField(max_length=200)
    catagories=models.ForeignKey(catagory,on_delete=models.CASCADE,default=1)
    Image=models.ImageField(upload_to='uploads/product/',blank='')
    In_stock = models.IntegerField(blank='',null=True)

    is_sale= models.BooleanField(default=False)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2,null=True)

    def __str__(self):
        return self.name
    



class order(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    customer=models.ForeignKey(customer,on_delete=models.CASCADE)
    address=models.CharField(max_length=100)
    phone=models.CharField(max_length=15)
    quantity=models.IntegerField(default=1)
    date=models.DateField(default=datetime.now)
    status=models.BooleanField(default=False)

    def __str__(self):
        return self.product













# class cartItem(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveBigIntegerField(default=1)

#     @property
#     def total_price(self):
#         return self.product.price * self.quantity
    
#     def __str__(self):
#         return f"{self.product.name} X {self.quantity}"