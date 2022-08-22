from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotFound
import json, datetime
from django.views import View
from django.views.generic import ListView, CreateView

from store.models import Order, OrderItem, Product, ShippingAddress

class store(ListView):

    model = Product
    template_name = 'store/store.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            customer = self.request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            context['order'] = order
        else:
            context['order'] = {'get_cart_items':0, 'shipping':False}
        return context


class updateItem(View):
    def get(self, request):
        return HttpResponseNotFound(request)
    
    def post(self, request):
        data = json.loads(request.body)
        productId = data['productId']
        action = data['action']

        customer = request.user.customer
        product = Product.objects.get(pk=productId)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
        if action == 'add':
            orderItem.quantity += 1
        elif action == 'remove':
            orderItem.quantity -= 1
        orderItem.save()

        data = dict()
        if orderItem.quantity <= 0:
            orderItem.delete()
            data['remove'] = True
        else:          
            data['total-items'] = order.get_cart_items
            data['total-price'] = order.get_cart_total
            data['item-id'] = orderItem.id
            data['item-quantity'] = orderItem.quantity
            data['item-price'] = orderItem.get_total

        return JsonResponse(data)


def processOrder(request):

    transactionId = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        # check the order data
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        order.transaction_id = str(transactionId)
        total = order.get_cart_total
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
    else:
        print('User is not logged in..')

    return JsonResponse('payment submitted..', safe=False)

# class processOrder(CreateView):
#     pass


class cart(View):
    def get(self, request):

        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
        else:
            items = []
            order = {'get_cart_items':0, 'get_cart_total':0, 'shipping':False}

        context = {'items':items, 'order':order}
        return render(request, 'store/cart.html', context)


class checkout(View):
    def get(self, request):
        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
        else:
            items = []
            order = {'get_cart_items':0, 'get_cart_total':0, 'shipping':False}

        context = {'items':items, 'order':order}
        return render(request, 'store/checkout.html', context)
