from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product, CartItem
from django.contrib.sessions.models import Session

def shop(request):
    products = Product.objects.all()
    return render(request, 'shop/shop.html', {'products': products})

def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)

    # Get cart from session
    cart = request.session.get('cart', {})

    if product_id in cart:
        # If item already in cart, increase quantity
        cart[product_id]['quantity'] += 1
    else:
        # If item is not in cart, add it with quantity 1
        cart[product_id] = {
            'name': product.name,
            'price': str(product.price),
            'quantity': 1
        }

    request.session['cart'] = cart
    return redirect('cart')

def cart(request):
    cart = request.session.get('cart', {})
    total_price = sum(float(item['price']) * item['quantity'] for item in cart.values())
    return render(request, 'shop/cart.html', {'cart': cart, 'total_price': total_price})

def update_cart(request, product_id):
    cart = request.session.get('cart', {})

    if product_id in cart:
        quantity = int(request.POST.get('quantity'))
        if quantity <= 0:
            del cart[product_id]
        else:
            cart[product_id]['quantity'] = quantity
    request.session['cart'] = cart
    return redirect('cart')

def checkout(request):
    return render(request, 'shop/checkout.html')
