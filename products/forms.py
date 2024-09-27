from django import forms as form
from django.contrib.auth import get_user_model
from .models import *

User = get_user_model()

class ProductForm(form.ModelForm):
    class Meta:
        model = Products
        fields = ['name', 'description', 'price', 'image', 'stock']
    
    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get('price')
        stock = cleaned_data.get('stock')

        
        if price < 0:
            raise form.ValidationError('Price cannot be negative')
        
        if stock < 0:
            raise form.ValidationError('Stock cannot be negative')
        
        return cleaned_data

class ReviewForm(form.ModelForm):
    class Meta:
        model = Review
        fields = ['review', 'rating']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['review'].widget = form.Textarea()
        self.fields['rating'].widget = form.NumberInput()
    
    def save(self, product, user, seller, commit=True):
        review = super().save(commit=False)
        review.product = product
        review.user = user
        review.seller = seller
        if commit:
            review.save()
        return review


class ShippingForm(form.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['address', 'city', 'postal_code', 'country']

    def cleaned_data(self):
        cleaned_data = super().clean()
        address = cleaned_data.get('address')
        city = cleaned_data.get('city')
        postal_code = cleaned_data.get('postal_code')
        country = cleaned_data.get('country')

        if not address:
            raise form.ValidationError('Address is required')

        if not city:
            raise form.ValidationError('City is required')

        if not postal_code:
            raise form.ValidationError('Postal code is required')

        if not country:
            raise form.ValidationError('Country is required')

        return cleaned_data

class PaymentForm(form.Form):
    payment = form.ChoiceField(choices=[('PayPal', 'PayPal')])


class OrderForm(form.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'