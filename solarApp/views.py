from django.shortcuts import render, redirect
from .models import Products,profile
from django.views.generic import ListView,CreateView,DetailView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForms, ChangePasswordForm,UserProfileForm
import json
from cart.cart import Cart
# Create your views here.

# class ProductListView(ListView):
#     model = Products
#     # template_name = 'Product_list.html'  # The template for displaying the product list
#     # context_object_name = 'products'  # Context variable to be used in the template

# def home(request):                    ---> this is for main solar page

#     return render(request, 'home.html', {})




def product_list(request):
    # Query all products from the database
    products = Products.objects.all()

    # Pass the products to the template
    return render(request, 'shop.html', {'products': products})

def product(request,pk):
    product=Products.objects.get(id=pk)
    return render(request,'product.html',{'product':product})


def about_page(request):
    return render(request,'about.html',{})

#Login and logout user
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)

            #do some shoping cart stuff
            current_user = profile.objects.get(user__id=request.user.id)            #getting current user profile
            #get the saved cart from database
            saved_cart=current_user.old_cart
            #convet database string to python dictionary 
            if saved_cart:
                #convert to dictionary using JSON

                converted_cart= json.loads(saved_cart)

                #add the loaded cart dictionary to our session
                #get the cart
                cart=Cart(request)
                #loop through cart and add items from database
                for key,value in converted_cart.items():
                    cart.DB_add(product=key,quantity=value)                 #this DB_add is in cart.cart.py file to initialize


            messages.success(request,("you have been login"))
            return redirect('home')
        else:
            messages.success(request,("Invalid username/password"))
            return redirect('login')

    else:
        return render(request, 'login.html',{})
    
def logout_user(request):
    logout(request)
    messages.success(request,('You have been logout, thank you'))
    return redirect('home')


def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data['username']
            password=form.cleaned_data['password1']
            #login user
            user=authenticate(username=username,password=password)
            login(request,user)
            messages.success(request,('You have been SignUp successfuly'))
            return redirect('home')
        else:
            # messages.success(request,('Woops... there was problem'))
            for error in list(form.errors.values()):                    # this code is for showing error if form is not valid
                messages.error(request,error)
                return redirect('register')
    else:
        return render(request,'register.html',{'form':form})
    

def update_info(request):
    if request.user.is_authenticated:
        current_user=profile.objects.get(user__id=request.user.id)                      #search for the profile that have user__id of our request user id(because sometime user id and profile id did't match)
        form=UserProfileForm(request.POST or None,instance=current_user)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            for error in list(form.errors.values()):                    # this code is for showing error if form is not valid
                    messages.error(request,error)
                    return redirect('update_info')
        return render(request,'update_info.html',{'form':form})
    else:
        messages.success(request,'Loggin Required')
        return redirect('login')    

        





def update_user(request):
   if request.user.is_authenticated:
       current_user = User.objects.get(id=request.user.id)              #get the current user
       user_form = UpdateUserForms(request.POST or None, instance=current_user)      #instance is for ,current user's information already in form
       if user_form.is_valid():
           user_form.save()
           login(request, current_user)
           messages.success(request, 'your profile has been updated')
           return redirect('home')
       return render(request,'update_user.html',{'user_form':user_form})
   else:
       messages.success(request, 'you must be logged in to access this')
       return redirect('home')

      
def update_password(request):
    if request.user.is_authenticated:
        current_user=User.objects.get(id=request.user.id)
        #did user fill the form
        if request.method == 'POST':
            #get the form
            form=ChangePasswordForm(current_user,request.POST)
            #check form is valid
            if form.is_valid():
                form.save()
                messages.success(request,'Your Password Has Been Changed')
                login(request,current_user)
                return redirect('home')
            else:
                for error in list(form.errors.values()):                    # this code is for showing error if form is not valid
                    messages.error(request,error)
                    return redirect('update_password')
        else:
            form=ChangePasswordForm(current_user)    
            return render(request,'update_password.html',{'form':form})
    else:
        messages.success(request,'You must be logged in')
        return redirect('home')


def search(request):
    #determine if the form filled out
    if request.method == 'POST':
        searched=request.POST['Searched']               #data of 'Searched' comes from name="Searched" in html
        #query the product db model
        searched=Products.objects.filter(name__icontains=searched)          #icontains is case insensitive   || if want to filtter more we have to use from django.db.models import Q searched=Products.objects.filter(Q(name__icontains=searched) | Q(description__icontain=searched))   
        #test for null
        if not searched:
            messages.success(request, 'product not found')
            return render(request,'search.html',{})
        else:
            return render(request,'search.html',{'searched':searched})
    else:
        return render(request,'search.html',{})
























class ShopDetailView(DetailView):
    model=Products
    fields='__all__'
    success_url=reverse_lazy('home')

class ShopUpdateView(UpdateView):
    model= Products
    fields='__all__'
    success_url=reverse_lazy('home')

class ShopCreateView(CreateView):
    model=Products
    fields='__all__'
    success_url= reverse_lazy('home')
