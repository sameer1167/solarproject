from django.shortcuts import render,get_object_or_404 ,redirect
from .cart import Cart
from solarApp.models import Products
from django.http import JsonResponse
from django.contrib import messages

# Create your views here.
def cart_summary(request):
    cart= Cart(request)         #specific user looking up the product
    cart_products=cart.get_product
    quantities=cart.get_quantity
    totals=cart.cart_total()
    return render(request,'cart_summary.html', {'cart_products':cart_products,'quantities':quantities, 'totals':totals })

def cart_add(request):
    #get the cart
    cart= Cart(request)         #specific user looking up the product
    #test for post
    if request.POST.get('action') == 'post':       # -->   action in jquery, when button is clicked(PoSTed)
        #get the stuff
        product_id= int(request.POST.get('product_id'))         #takes product id data when button clicked
        product_qty= int(request.POST.get('product_qty'))          #takes product quantity data when button clicked
        #lookup product in DB
        product=get_object_or_404(Products, id=product_id )         
        #save to session
        
        cart.add(product=product, quantity=product_qty)           #product with ID is added to cart
        #return response
        cart_quantity= cart.__len__()           #--> length of cart(kitna product cart mai add hua hai)

        # response = JsonResponse({'Product Name :' :product.name})   --->    #This to check, product is added to cart in back-end
        response = JsonResponse({'qty' :cart_quantity})
        messages.success(request,('item added to cart...'))
        return response

    


def cart_delete(request):
    cart=Cart(request)
     #test for post
    if request.POST.get('action') == 'post':       # -->   action in jquery, when button is clicked(PoSTed)
        #get the stuff
        product_id= int(request.POST.get('product_id'))         #takes product id data when button clicked
        cart.delete(product=product_id)

        response=JsonResponse({'prod':product_id})          #this dictionary we passed in response dosn't mean anything, we passed because in jsonresponse we have to pass things
        messages.success(request,('item removed from shoping cart...'))
        return response
    

def cart_update(request):
    cart=Cart(request)
     #test for post
    if request.POST.get('action') == 'post':       # -->   action in jquery, when button is clicked(PoSTed)
        #get the stuff
        product_id= int(request.POST.get('product_id'))         #takes product id data when button clicked
        product_qty= int(request.POST.get('product_qty'))             #takes product quantity data when button clicked
        
        cart.update(product=product_id , quantity=product_qty)
        
        response = JsonResponse({'qty':product_qty})
        messages.success(request,('Your cart has been updated...'))
        return response
        # return redirect(cart_summary)
        
