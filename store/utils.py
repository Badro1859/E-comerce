
import json
from .models import *

def cartData(request, withItems=True):
    items = {}
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        if withItems:
            items = order.orderitem_set.all()
    else:
        cart = cookieCart(request.COOKIES['cart'], withItems)
        order = cart['order']
        if withItems:
            items = cart['items']

    context = {'items':items, 'order':order}
    return context

# for not logged user
# cookieCart return the order and items informations from cookieData
def cookieCart(cookieData, withItems=True):
    try:
        cart = json.loads(cookieData) 
    except:
        cart = {}

    items = []
    order = {'get_cart_items':0, 'get_cart_total':0, 'shipping':False}
    
    b = True
    for p in cart:
        try:
            product = Product.objects.get(pk=p)
            order['get_cart_items'] += cart[p]['quantity']

            if withItems:
                total = product.price * cart[p]['quantity']
                order['get_cart_total'] += total
                if (b and product.digital == False):
                    order['shipping'] = True
                    b = False

                item = {
                    'product':product,
                    'quantity':cart[p]['quantity'],
                    'get_total':total,
                }
                items.append(item)
        except:
            pass
    
    return {'items':items, 'order':order}

# checkout guest order data from cookieData
def guestOrder(cookies, form):

    # get data of the customer (guest-User) and create it
    name = form['name']
    email = form['email']

    customer, created = Customer.objects.get_or_create(email=email)
    customer.name = name
    customer.save()

    # create the order instance
    order = Order.objects.create(customer=customer, complete=False)

    # create all orderItem form items of the cookieCart fct
    items = cookieCart(cookies)['items']

    for item in items:
        OrderItem.objects.create(
            product=item['product'],
            order=order,
            quantity=item['quantity'],
        )
    
    return customer, order