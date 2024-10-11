from django.shortcuts import render
from django.http import HttpResponse
# from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm, UserLoginForm, SellerRegisterForm
from django.contrib.auth import get_user_model
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from products.models import Products
from django.contrib.auth.decorators import login_required
from products.models import Category
from products.models import Products, Order, Review

User = get_user_model()
from django.db.models import Min, Max
from django.shortcuts import render, get_object_or_404
from .models import Profile

from django.db.models import Q  # Import Q for more complex queries


def index(request):
    # Get price range from the database
    price_range = Products.objects.aggregate(min_price=Min('price'), max_price=Max('price'))
    
    # Set defaults to None initially (so placeholders show when form is empty)
    min_price = request.GET.get('min_price') or None
    max_price = request.GET.get('max_price') or None
    
    # Use DB min/max prices only if user input is not provided
    price_min = min_price if min_price is not None else price_range['min_price']
    price_max = max_price if max_price is not None else price_range['max_price']
    
    category_list = Category.objects.all()
    category = request.GET.get('category') 
    search_query = request.GET.get('search')
    
    # Fetch all products initially
    products = Products.objects.all()
    
    # Apply search query first, regardless of category
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    # Apply category filter only if no search query is provided
    elif category:
        products = products.filter(category=category)

    # Apply price filter
    if price_min or price_max:
        products = products.filter(price__gte=price_min, price__lte=price_max)

    context = {
        'products': products,
        'category_list': category_list,
        'category': category,
        'selected_category': category,
        'search_query': search_query,
        'price_min': min_price,
        'price_max': max_price,
        'min_price': price_range['min_price'],
        'max_price': price_range['max_price'],
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
        print(form)  # Debug: Check form data
        if form.is_valid():
            user = form.get_user()
            print(user)  # Debug: Check if user is fetched correctly
            login(request, user)
            return redirect('index')  # Redirect after successful login
    else:
        form = UserLoginForm()
    return render(request, 'auth/login.html', {'form': form})

def Logout(request):
    logout(request)
    return redirect('login')



@login_required
def seller_register(request):
    # Ensure the user is authenticated
    if request.method == 'POST':
        seller_form = SellerRegisterForm(request.POST)

        if seller_form.is_valid():
            # Get the currently logged-in user
            user = request.user
            user.is_seller = True  # Mark user as a seller
            user.save()

            # Create the Seller profile and link it to the logged-in user
            seller = seller_form.save(commit=False)
            seller.user = user  # Link the seller to the user
            seller.save()

            return redirect('index')  # Redirect to index after registration
    else:
        seller_form = SellerRegisterForm()

    return render(request, 'auth/seller_register.html', {'seller_form': seller_form})


@login_required
def profile_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    
    # Get products posted by the logged-in user
    user_products = Products.objects.filter(seller=request.user)
    user_orders = Order.objects.filter(user=request.user)
    user_reviews = Review.objects.filter(user=request.user)

    context = {
        'profile': profile,
        'products': user_products,  # Updated to include only products posted by the user
        'orders': user_orders,
        'reviews': user_reviews,
        'profile_picture': profile.profile_picture,
    }
    
    return render(request, 'profile/profile_view.html', context)



