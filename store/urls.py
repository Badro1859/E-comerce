from django.urls import path
from django.conf.urls.static import static
from _packages import settings

from . import views

app_name='store'
urlpatterns = [
    path('', views.store.as_view(), name='store'),
    path('product/<int:pk>', views.ProductItem.as_view(), name='product'),

    path('cart/', views.cart.as_view(), name='cart'),
    path('checkout/', views.checkout.as_view(), name='checkout'),
    
    path('update-item/', views.updateItem.as_view(), name='update-item'),
    path('process-order/', views.processOrder, name='process-order'),
]
if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
