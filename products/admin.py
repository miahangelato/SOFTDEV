from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Products)
admin.site.register(cartItem)
admin.site.register(Review)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Category)
