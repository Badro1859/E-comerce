from django.contrib import admin

from store.models import Customer, OrderItem, Product, Order, ShippingAddress

# Register your models here.

admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
