from django.urls import path

from .views import (cart_view, cart_add_view, cart_update_view, cart_remove_view, cart_clear_view)

urlpatterns = [
    path('cart/', cart_view, name='cart_url'),
    path('cart/add/<int:pk>/', cart_add_view, name='cart_add_url'),
    path('cart/update/<int:pk>/', cart_update_view, name='cart_update_url'),
    path('cart/remove/<int:pk>/', cart_remove_view, name='cart_remove_url'),
    path('cart/clear/', cart_clear_view, name='cart_clear_url'),
]