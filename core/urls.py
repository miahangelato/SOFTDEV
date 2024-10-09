from django.urls import path
from .views import *

urlpatterns = [
    path('home/', index, name='index'),
    path('register/', register, name='register'),
    path('login/', UserLogin, name='login'),
    path('logout/', Logout, name='logout'),
    path('seller_register/', seller_register, name='seller_register'),
    path('profile/', profile_view, name='profile'),

] 