from django.shortcuts import render, redirect
from .forms import ShippingAddressForm
from .models import ShippingAddress
from django.contrib import messages

# Create your views here.
def payment_success(request):

    return render(request,'payment/payment_success.html',{})


def shipping_address(request):
    if request.user.is_authenticated:
        current_shipping_user=ShippingAddress.objects.get(id=request.user.id)
        shipping_form=ShippingAddressForm(request.POST or None,instance=current_shipping_user)
        if shipping_form.is_valid():
            shipping_form.save()
            messages.success(request,'Shipping Address Updated Successfully')
            return redirect('home')
        else:
            for error in list(shipping_form.errors.values()):                    # this code is for showing error if form is not valid
                messages.error(request,error)
                return redirect('shipping_address')
        return render(request,'payment/shippingform.html',{'shipping_form':shipping_form})
    return render(request,'payment/shippingform.html',{})