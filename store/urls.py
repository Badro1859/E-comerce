from django.urls import path
from django.conf.urls.static import static
from _packages import settings

from . import views

app_name='store'
urlpatterns = [
    path('', views.store.as_view(), name='store'),
    path('cart/', views.cart.as_view(), name='cart'),
    path('checkout', views.checkout.as_view(), name='checkout'),
]
if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
