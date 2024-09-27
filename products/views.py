from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse
from .forms import *
from django.contrib.auth.decorators import login_required


# def listProducts(request):
#     products = Products.objects.all()
#     return render(request, 'index.html', {'products': products})

@login_required
def viewProduct(request, pk):
    product = Products.objects.get(pk=pk)
    obj_list = Review.objects.filter(product=product)
    print(obj_list)
    context = {
        'product': product,
        'reviews': obj_list
    }
    return render(request, 'products/productsDetail.html', context)

def createProduct(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False) 
            product.seller = request.user 
            product.save()  
            return redirect('/')  
    else:
        form = ProductForm()
    
    return render(request, 'products/createProduct.html', {'form': form})


def Updateproduct(request, pk):
    product = Products.objects.get(pk=pk)
    if request.user != product.seller:
        return HttpResponse("You don't have permission to update this product.")

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/updateProduct.html', {'form': form})

def deleteProduct(request, pk):
    product = Products.objects.get(pk=pk)

    if request.user != product.seller:
        return HttpResponse("You don't have permission to delete this product.")
    product.delete()
    return redirect('/')




def createReview(request, pk):
    product = Products.objects.get(pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        print(form)
        if form.is_valid():
            review = form.save(product, request.user, product.seller)
            return redirect('viewProduct', pk=pk)
    else:
        form = ReviewForm()
    return render(request, 'products/createReview.html', {'form': form})

def deleteReview(request, pk):
    review = Review.objects.get(pk=pk)
    if request.user != review.user:
        return HttpResponse("You don't have permission to delete this review.")
    review.delete()
    return redirect('viewProduct', pk=review.product.pk)


def UserCartList(request):
    cart = request.session.get('cart', {})
    print(cart)
    total_cost = 0
    for key, item in cart.items():
        item['total_price'] = item['price'] * item['quantity']
        total_cost += item['total_price']
    context = {
        'cart': cart,
        'total_cost': total_cost
    }
    return render(request, 'products/cart.html', context)

def addToCart(request, pk):
    # Retrieve the product by its primary key
    product = Products.objects.get(pk=pk)

    # Check if 'cart' exists in session, if not, initialize it as a dictionary
    cart = request.session.get('cart', {})

    # If cart is an integer (from previous session state), reset it to an empty dict
    if isinstance(cart, int):
        cart = {}

    # Check if the product is already in the cart
    if str(pk) in cart:
        # If the product was stored as an integer, update the structure to store more info
        if isinstance(cart[str(pk)], int):
            cart[str(pk)] = {
                'name': product.name,
                'price': product.price,
                'quantity': cart[str(pk)] + 1,
                'description': product.description,
                'image': product.image.url
            }
        else:
            # If the product is already in the correct structure, increment the quantity
            cart[str(pk)]['quantity'] += 1
    else:
        # Otherwise, add the product to the cart with a quantity of 1
        cart[str(pk)] = {
            'name': product.name,
            'price': product.price,
            'quantity': 1,
            'description': product.description,
            'image': product.image.url
        }

    # Update the session cart
    request.session['cart'] = cart

    # For debugging: print the cart content
    print('Cart:', request.session['cart'])

    # Redirect to the 'cart' view
    return redirect('cart')





def removeCartItem(request, pk):
    # Retrieve the product by its primary key
    product = Products.objects.get(pk=pk)

    # Get the cart from session
    cart = request.session.get('cart', {})

    # Check if the product is in the cart
    if str(pk) in cart:
        # If the product was stored as an integer, reset the cart item structure
        if isinstance(cart[str(pk)], int):
            cart[str(pk)] = {
                'name': product.name,
                'price': product.price,
                'quantity': cart[str(pk)],
                'description': product.description,
                'image': product.image.url
            }

        # If the product quantity is more than 1, decrement the quantity
        if cart[str(pk)]['quantity'] > 1:
            print('bawas')
            cart[str(pk)]['quantity'] -= 1
        else:
            # If the quantity is 1 or less, remove the product from the cart
            del cart[str(pk)]

    # Update the session with the modified cart
    request.session['cart'] = cart

    # Redirect to the cart view
    return redirect('cart')

def shipping_view(request):
    form = ShippingForm()
    
    if not request.user.is_authenticated:
        return redirect('login')


    if request.method == 'POST':
        print('Shipping', request.POST)
        form = ShippingForm(request.POST)
        shipping = request.session.get('shipping', {})
        if form.is_valid():
            for k, v in form.cleaned_data.items():
                shipping[k] = v

                print(shipping)
            return redirect('payment')
        request.session['shipping'] = shipping
    return render(request, 'cart/shipping.html', {'form': form})

def payment_view(request):
    form = PaymentForm()

    # print(payment)
    # print(request.POST['payment'])
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        payment = request.session.get('payment', {})
        if form.is_valid():
            print(form.cleaned_data)
            payment['payment'] = form.cleaned_data['payment']
            print(payment)
            return redirect('confirm_order')
        request.session['payment'] = payment
    return render(request, 'cart/payment.html', {'form': form})

def confirm_order(request):
    if not request.user.is_authenticated:
        return redirect('login')
    cart = request.session.get('cart')
    shipping = request.session.get('shipping')
    payment = request.session.get('payment')
    total_cost = 0
    print('confirm_order', cart)
    print('confirm_order', shipping)
    print('confirm_order', payment)

    if not cart:
        return redirect('cart')

    for key, item in cart.items():
        item['total_price'] = item['price'] * item['quantity']
        total_cost += item['total_price']

    context = {
        'cart': cart,
        'shipping': shipping,
        'payment': payment,
        'total_cost': total_cost
    }
    return render(request, 'cart/confirm_order.html', context)

def order_complete(request):
    if not request.user.is_authenticated:
        return redirect('login')
    cart = request.session.get('cart', {})
    shipping = request.session.get('shipping', {})
    payment = request.session.get('payment', {})
    total_cost = 0
    print(cart)

    if not cart or not shipping or not payment:
        return redirect('cart')

    else:
        for key, item in cart.items():
            item['total_price'] = item['price'] * item['quantity']
            total_cost += item['total_price']
        order = Order.objects.create(
            user=request.user,
            payment_method=payment['payment'],
            total_price=total_cost,
            is_paid=True
        )

        shipping = ShippingAddress.objects.create(
            order=order,
            address=shipping['address'],
            city=shipping['city'],
            postal_code=shipping['postal_code'],
            country=shipping['country']
        )

        for key, item in cart.items():
            product = Products.objects.get(pk=key)
            OrderItem.objects.create(
                order=order,
                product=product,
                name=product.name,
                price=item['price'],
                qty=item['quantity'],
            )
            product.stock -= item['quantity']
            product.save()
        request.session['cart'] = {}
        request.session['shipping'] = {}
        request.session['payment'] = {}
        return redirect('index')
    # return render(request, 'cart/confirm_order.html', context)