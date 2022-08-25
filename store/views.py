from itertools import product
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotFound
import json, datetime
from django.views import View
from django.views.generic import ListView, CreateView, DetailView

from store.models import *
from store.utils import cartData, cookieCart, guestOrder

class store(ListView):

    model = Product
    template_name = 'store/store.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        search = self.request.GET.get('search-area') or ''
        if (search):
            context['products'] = context['products'].filter(name__contains=search)
        
        context['search_area'] = search
        context['order'] = cartData(self.request, False)['order']
        return context


class ProductItem(DetailView):
    model = Product
    template_name = "store/productItem.html"
    context_object_name = "product"


class cart(View):
    def get(self, request):
        context = cartData(self.request)
        return render(request, 'store/cart.html', context)


class checkout(View):
    def get(self, request):
        context = cartData(self.request)
        return render(request, 'store/checkout.html', context)


def processOrder(request):

    data = json.loads(request.body)

    if request.user.is_authenticated:
        # check the order data
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        
    else:
        print('User is not logged in..')
        customer, order = guestOrder(request.COOKIES['cart'], data['form'])

    transactionId = datetime.datetime.now().timestamp()
    order.transaction_id = str(transactionId)
    # total = order.get_cart_total
    order.complete = True
    order.save()

    # check the shipping data
    if order.shipping:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )
        
    return JsonResponse('payment submitted..', safe=False)


class updateItem(View):
    def get(self, request):
        return HttpResponseNotFound(request)
    
    def post(self, request):
        data = json.loads(request.body)
        productId = data['productId']
        action = data['action']

        # authenticated user
        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)

            product = Product.objects.get(pk=productId)
            orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
            if action == 'add':
                orderItem.quantity += 1
            elif action == 'remove':
                orderItem.quantity -= 1
            orderItem.save()

            if orderItem.quantity <= 0:
                orderItem.delete()
                data['remove'] = True
            else:
                data['total-price'] = order.get_cart_total
                data['item-quantity'] = orderItem.quantity
                data['item-price'] = orderItem.get_total
            data['total-items'] = order.get_cart_items
        else:          
            result = cookieCart(request.COOKIES['cart'])
            
            data['total-items'] = result['order']['get_cart_items']
            data['total-price'] = result['order']['get_cart_total']

            for item in result['items']:
                if (item['product'].id == int(productId)):
                    data['item-quantity'] = item['quantity']
                    data['item-price'] = item['get_total']
                    break

        return JsonResponse(data)
