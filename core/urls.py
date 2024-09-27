from django.urls import path
from .views import *

urlpatterns = [
    path('home/', index, name='index'),
    path('register/', register, name='register'),
    path('', UserLogin, name='login'),
    path('logout/', Logout, name='logout'),

] 