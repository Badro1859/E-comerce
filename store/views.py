from django.shortcuts import render

from django.views import View
from django.views.generic import ListView

from store.models import Order, Product

class store(ListView):

    model = Product
    template_name = 'store/store.html'
    context_object_name = 'products'


class cart(View):
    def get(self, request):

        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
        else:
            items = []
            order = {'get_cart_items':0, 'get_cart_total':0}

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
            order = {'get_cart_items':0, 'get_cart_total':0}

        context = {'items':items, 'order':order}
        return render(request, 'store/checkout.html', context)
