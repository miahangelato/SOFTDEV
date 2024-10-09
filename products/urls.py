from django.urls import path
from .views import *

urlpatterns = [
    path('create/', createProduct, name='createProduct'),
    # path('list/', listProducts, name='listProducts'),
    path('list/<int:pk>/', viewProduct, name='viewProduct'),
    path('post/', createProduct, name='createProduct'),
    path('update/<int:pk>/', Updateproduct, name='updateProduct'),
    path('delete/<int:pk>/', deleteProduct, name='deleteProduct'),
    path('cart/', UserCartList, name='cart'),
    path('cart/<int:pk>/', addToCart, name='addToCart'),
    path('cart/delete/<int:pk>/', removeCartItem, name='removeCartItem'),
    path('review/<int:pk>/', createReview, name='review'),
    path('review/delete/<int:pk>/', deleteReview, name='deleteReview'),
    path('shipping/', shipping_view, name='shipping'),
    path('confirm-order/', confirm_order, name='confirm_order'),
    path('order-complete/', order_complete, name='order_complete'),
]