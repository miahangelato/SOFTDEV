from django.shortcuts import render
from django.http import HttpResponse
# from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth import get_user_model
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from products.models import Products
from products.models import Category

User = get_user_model()
from django.db.models import Min, Max

from django.db.models import Q  # Import Q for more complex queries


def index(request):
    price_range = Products.objects.aggregate(min_price=Min('price'), max_price=Max('price'))
    min_price = price_range['min_price']
    max_price = price_range['max_price']
    category_list = Category.objects.all()
    category = request.GET.get('category') 
    price_min = request.GET.get('minPrice', min_price)
    price_max = request.GET.get('maxPrice', max_price)
    search_query = request.GET.get('search')
    products = Products.objects.all()
    if category:
        products = products.filter(category=category)
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    if price_min or price_max:
        products = products.filter(price__gte=price_min, price__lte=price_max)

    context = {
        'products': products,
        'category_list': category_list,
        'category': category,
        'selected_category': category,
        'search_query': search_query,   
        'price_min': price_min,
        'price_max': price_max,
        'min_price': min_price,
        'max_price': max_price,
    }
    return render(request, 'index.html', context)



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = UserRegisterForm()
    return render(request, 'auth/register.html', {'form': form})

def UserLogin(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST or None)
        print(form)
        if form.is_valid():
            user = form.get_user()
            print(user)
            login(request, user)
            return redirect('index')
    else:
        form = UserLoginForm()
    return render(request, 'auth/login.html', {'form': form})

def Logout(request):
    logout(request)
    return redirect('login')

