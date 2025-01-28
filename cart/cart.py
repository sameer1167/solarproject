from solarApp.models import Products, profile


class Cart():
    def __init__(self,request):
        self.session = request.session
        #get request
        self.request = request
        
        #get the current session key
        cart=self.session.get('session_key')

        #if user is new, create new session
        if 'session_key' not in request.session:
            cart=self.session['session_key'] = {}

        #make sure cart is avilable on all pages of site
        self.cart=cart 

    def add(self,product,quantity):
        product_id=str(product.id)
        product_qty=str(quantity)
        #logic
        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'Price': str(product.price)}
            self.cart[product_id] = int(product_qty)

        self.session.modified=True

        #deal with logged in user
        if self.request.user.is_authenticated:
            #get the current profile 
            current_user = profile.objects.filter(user__id=self.request.user.id)            #we use filter insted of get because easy to update
            #convert {'3':2 , '4':5} to {"3":2 , "4":5}         because we have to save this python dictionary information to database in json format
            carty = str(self.cart)                  #this will turn {'3':2 , '4':5} to "{'3':2 , '4':5}"
            carty = carty.replace('\'' , '\"')
            #save the carty to the profile model
            current_user.update(old_cart=str(carty))            # it is easy to update model using filter

    def DB_add(self,product,quantity):                  #thid DB_add function is for adding pre-existing cart information(dictionary) saved in database
        product_id=str(product)
        product_qty=str(quantity)
        #logic
        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'Price': str(product.price)}
            self.cart[product_id] = int(product_qty)

        self.session.modified=True

        #deal with logged in user
        if self.request.user.is_authenticated:                      #we did this function again because if user is logged out and add something in cart will remain in the cart after loggin 
            #get the current profile 
            current_user = profile.objects.filter(user__id=self.request.user.id)            #we use filter insted of get because easy to update
            #convert {'3':2 , '4':5} to {"3":2 , "4":5}         because we have to save this python dictionary information to database in json format
            carty = str(self.cart)                  #this will turn {'3':2 , '4':5} to "{'3':2 , '4':5}"
            carty = carty.replace('\'' , '\"')
            #save the carty to the profile model
            current_user.update(old_cart=str(carty))            # it is easy to update model using filter



    def __len__(self):
        return len(self.cart)
    
    def get_product(self):
        #get id from cart
        product_ids=self.cart.keys()                        #--> get all the id(keys) 
        #use ids to look up the products in database
        products=Products.objects.filter(id__in=product_ids)
        #return those looked up products
        return products
    
    def cart_total(self):
        #get product ids
        product_ids= self.cart.keys()
        #look up those keys in our products database
        products= Products.objects.filter(id__in=product_ids)
        #get quantities
        our_cart=self.cart
        #start counting from 0
        total=0
        for key, value in our_cart.items():
            #convert key string into int to do calculation
            key=int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total = total + (product.sale_price * value)
                    else:
                        total = total + (product.price * value)
        return total




    def get_quantity(self):
        quantities=self.cart
        return quantities
    
    def update(self,product,quantity):
        product_id = str(product)
        product_qty = int(quantity)
        #get the cart
        our_cart=self.cart
        #to update dictionary/cart                      because cart is a dictionary and looks like {'3':2 , '4':5} thats why product_id and product_qty in line 46,47 is str and int
        our_cart[product_id] = product_qty
        #           key             value
        self.session.modified = True

        #deal with logged in user
        if self.request.user.is_authenticated:
            #get the current profile 
            current_user = profile.objects.filter(user__id=self.request.user.id)            #we use filter insted of get because easy to update
            #convert {'3':2 , '4':5} to {"3":2 , "4":5}         because we have to save this python dictionary information to database in json format
            carty = str(self.cart)                  #this will turn {'3':2 , '4':5} to "{'3':2 , '4':5}"
            carty = carty.replace('\'' , '\"')
            #save the carty to the profile model
            current_user.update(old_cart=str(carty))            # it is easy to update model using filter


        thing=self.cart             #for our new updated cart
        return thing 
    
    def delete(self,product):
        product_id = str(product)
        #delete from dictionary/cart
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

        #deal with logged in user
        if self.request.user.is_authenticated:
            #get the current profile 
            current_user = profile.objects.filter(user__id=self.request.user.id)            #we use filter insted of get because easy to update
            #convert {'3':2 , '4':5} to {"3":2 , "4":5}         because we have to save this python dictionary information to database in json format
            carty = str(self.cart)                  #this will turn {'3':2 , '4':5} to "{'3':2 , '4':5}"
            carty = carty.replace('\'' , '\"')
            #save the carty to the profile model
            current_user.update(old_cart=str(carty))            # it is easy to update model using filter
