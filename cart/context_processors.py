from . cart import Cart

#create context processor so that cart data can work/view on all pages
def cart(request):
    #return the default data from our cart
    return {'cart':Cart(request)}