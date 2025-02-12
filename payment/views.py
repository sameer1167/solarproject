from django.shortcuts import render, redirect
from .forms import ShippingAddressForm,PaymentForm
from .models import ShippingAddress, order, orderItem
from django.contrib import messages
from cart.cart import Cart
from solarApp.models import Products, profile
import datetime


from django.core.mail import send_mail
from django.conf import settings

# Create your views here.


def orders(request,pk):
    if request.user.is_authenticated and request.user.is_superuser:
        #get the order
        orders= order.objects.get(id=pk)
        #get the order items
        items = orderItem.objects.filter(order=pk)

        if request.POST:
            status = request.POST['shipping_status']
            #check if status is true or false
            if status == 'true':
                #get the order
                orders = order.objects.filter(id=pk)
                #update the shipped status and date
                now = datetime.datetime.now()
                orders.update(shipped=True,date_shipped=now)
            else:
                #get the order
                orders = order.objects.filter(id=pk)
                #update the shipped status
                orders.update(shipped=False)
            messages.success(request,'Shipping status updated')
            return redirect('shipped_status')


        return render(request,'payment/orders.html',{'orders':orders, 'items':items})
    else:
        messages.success(request,'Access Denied ') 
        return redirect('home')
    




def shipped_status(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders_unshipped = order.objects.filter(shipped=False)
        orders_shipped = order.objects.filter(shipped=True)
        return render(request,'payment/shipped_status.html',{'orders_unshipped':orders_unshipped, 'orders_shipped':orders_shipped})
    else:
        messages.success(request,'Access Denied ') 
        return redirect('home')





def process_order(request):
    if request.POST:
        #get the cart items
        cart= Cart(request)         #specific user looking up the product
        cart_products=cart.get_product
        quantities=cart.get_quantity
        totals=cart.cart_total()


        #lets get billing info form from last page
        payment_form = PaymentForm(request.POST or None)
        #lets get shipping session data
        my_shipping = request.session.get('my_shipping')            #getting shipping information by sessions which is defined in line 36, 37
        

        #gather order info
        full_name = my_shipping['Full_name']
        #create shipping address from session info
        shipping_address = f"\n{my_shipping['address_1']}\n{my_shipping['address_2']}\n{my_shipping['city']}\n{my_shipping['state']}\n{my_shipping['zipcode']}\n{my_shipping['country']}"
        amount_paid = totals

        #create an order
        #getting the user
        if request.user.is_authenticated:
            #logged in
            user=request.user
            # create order
            create_order=order(user=user, full_name = full_name, shipping_address = shipping_address, amount_paid =  amount_paid)
            create_order.save()

            # Add order items
            # get order id
            order_id = create_order.pk

            #get product info
            for product in cart_products():                 #loop through the cart_product to get all different products ID's
                #get product ID
                product_id = product.id
                #get the product price
                if product.is_sale:
                    price=product.sale_price
                else:
                    price = product.price

                #get the quantities
                for key,value in quantities().items():
                    if int(key) == product.id:
                        #create order item
                        create_order_item = orderItem(order_id=order_id,product_id=product_id, user=user, quantity=value, price=price)
                        create_order_item.save()

                #clear cart items onces order is placed by deleting session key
                for key in list(request.session.keys()):
                    if key == 'session_key':
                        #delete the session key
                        del request.session[key]

                #clear cart items from database(old_cart fiels)
                #get the current user
                current_user = profile.objects.filter(user__id=request.user.id)
                #delete shopping cart from database(old_cart firld)
                current_user.update(old_cart="")



            # 📧 Send order confirmation email
            subject = "Order Confirmation"
            message = f"""
            Hi {user.first_name},

            Thank you for your order! Your order ID is {order_id}.

            Total Amount: ${amount_paid}
            Shipping Address:
            {shipping_address}

            Your order details:
            """
            for item in cart_products():
                message += f"\n- {item.name}  - ${item.price}"

            message += "\n\nWe will notify you once your order is shipped!"

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,  # Set this in settings.py
                [user.email],
                fail_silently=False,
            )

            messages.success(request, 'Your order has been placed successfully! A confirmation email has been sent.')
            return redirect('home')




            messages.success(request,'order placed ') 
            return redirect('home')

        else:
            #not logged in
            # create order
            create_order=order(full_name = full_name, shipping_address = shipping_address, amount_paid =  amount_paid)
            create_order.save()

            # Add order items
            # get order id
            order_id = create_order.pk

            #get product info
            for product in cart_products():                 #loop through the cart_product to get all different products ID's
                #get product ID
                product_id = product.id
                #get the product price
                if product.is_sale:
                    price=product.sale_price
                else:
                    price = product.price

                #get the quantities
                for key,value in quantities().items():
                    if int(key) == product.id:
                        #create order item
                        create_order_item = orderItem(order_id=order_id,product_id=product_id, quantity=value, price=price)
                        create_order_item.save()


                #clear cart items onces order is placed by deleting session key
                for key in list(request.session.keys()):
                    if key == 'session_key':
                        #delete the session key
                        del request.session[key]

            messages.success(request,'order placed ') 
            return redirect('home')

    else:
        messages.success(request,'Access Denied') 
        return redirect('home')





def billing_info(request):
    if request.POST:
        #get the cart items
        cart= Cart(request)         #specific user looking up the product
        cart_products=cart.get_product
        quantities=cart.get_quantity
        totals=cart.cart_total()

        #create a session with shipping info
        my_shipping= request.POST
        request.session['my_shipping'] = my_shipping

        # check to see if user is logged in
        if request.user.is_authenticated:
            #get the billing form
            billing_form=PaymentForm()
            return render(request,'payment/billing_info.html',{'cart_products':cart_products,'quantities':quantities, 'totals':totals, 'F_shipping_info':request.POST,'billing_form':billing_form})
        # check to see if user is not logged in
        else:
            #get the billing form
            billing_form=PaymentForm()
            return render(request,'payment/billing_info.html',{'cart_products':cart_products,'quantities':quantities, 'totals':totals, 'F_shipping_info':request.POST,'billing_form':billing_form})




        return render(request,'payment/billing_info.html',{'cart_products':cart_products,'quantities':quantities, 'totals':totals, 'F_shipping_form':F_shipping_form})
    else:
        messages.success(request,'Access Denied') 
        return redirect('home')
    




def checkout(request):
    cart= Cart(request)         #specific user looking up the product
    cart_products=cart.get_product
    quantities=cart.get_quantity
    totals=cart.cart_total()

    if request.user.is_authenticated:
        #checkout for logged in user
        #shipping user
        current_shipping_user=ShippingAddress.objects.filter(id=request.user.id).first()
        #shipping form
        F_shipping_form=ShippingAddressForm(request.POST or None,instance=current_shipping_user)
        return render(request,'payment/checkout.html', {'cart_products':cart_products,'quantities':quantities, 'totals':totals, 'F_shipping_form':F_shipping_form})
    else:
        #checkout for guest user
        #shipping form
        F_shipping_form=ShippingAddressForm(request.POST or None)
        
        return render(request,'payment/checkout.html', {'cart_products':cart_products,'quantities':quantities, 'totals':totals, 'F_shipping_form':F_shipping_form })




def payment_success(request):

    return render(request,'payment/payment_success.html',{})


def shipping_address(request):
    if request.user.is_authenticated:
        current_shipping_user=ShippingAddress.objects.filter(id=request.user.id).first()
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