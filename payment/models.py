from django.db import models
from django.contrib.auth.models import User
from solarApp.models import Products
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import datetime

# Create your models here.
class ShippingAddress(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True, blank=True)
    Full_name = models.CharField(max_length=100,null=True, blank=True)
    Email = models.EmailField(max_length=100,null=True, blank=True)
    address_1 = models.CharField(max_length=100,null=True, blank=True)
    address_2 = models.CharField(max_length=100,null=True, blank=True)
    city = models.CharField(max_length=100,null=True, blank=True)
    state = models.CharField(max_length=100,null=True, blank=True)
    zipcode = models.CharField(max_length=100,null=True, blank=True)
    country = models.CharField(max_length=100,null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    #don't pluralize the shippingAddress model
    class Meta:
        verbose_name_plural = 'Shipping Address'


    def __str__(self):
        return f'Shipping Address - {str(self.id)}'
    


    #creating a signal to create a shipping address for a user when a user is created
    #create the user shipping address by default when the user sign up
    def create_shipping(sender,instance, created,**kwargs):
        if created:
            user_shipping=ShippingAddress(user=instance)                    
            user_shipping.save()

    #automate the profile things
    post_save.connect(create_shipping, sender=User) 
    

    

#create order model
class order(models.Model):
    #foreign key to user model
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    full_name= models.CharField(max_length=100)
    shipping_address = models.TextField(max_length=1500)
    amount_paid = models.DecimalField(max_digits=14,decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)
    shipped = models.BooleanField(default=False)
    date_shipped = models.DateTimeField(blank=True, null=True)

    def __str__(self):                                      #for showing order id in admin panel
        return f'order - {str(self.id)}'

#auto add shipping date time
@receiver(pre_save,sender=order)
def set_shipped_date_on_update(sender,instance,**kwargs):
    if instance.pk:
        now = datetime.datetime.now()
        obj = sender._default_manager.get(pk=instance.pk)
        if instance.shipped and not obj.shipped:
            instance.date_shipped = now






#create orderItem model
class orderItem(models.Model):
    #foriegn key to order model
    order = models.ForeignKey(order,on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True)

    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=14,decimal_places=2)

    def __str__(self):                                      #for showing orderItem id in admin panel
        return f'Order Item - {str(self.id)}'