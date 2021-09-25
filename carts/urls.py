from django.urls import path
from carts.views import index, add_cart, decrease_cart, remove_item, increase_cart

urlpatterns = [
    path('', index, name='cart'),
    path('add_cart/<int:product_id>', add_cart, name='add_cart'),
    path('increase-product/<int:cart_item>', increase_cart, name='increase_cart'),
    path('decrease-product/<int:cart_item>', decrease_cart, name='decrease_cart'),
    path('remove-item/<int:cart_item>', remove_item, name='remove_cart_item'),
    # path('', 'carts.views.cart_detail', name='cart_detail'),
]