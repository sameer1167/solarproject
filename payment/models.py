from django.db import models
from django.contrib.auth.models import User

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