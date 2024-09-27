from django import forms as form
from django.contrib.auth import get_user_model
User = get_user_model()

class UserRegisterForm(form.Form):
    username = form.CharField(max_length=100)
    email = form.EmailField()
    password = form.CharField(widget=form.PasswordInput())
    password2 = form.CharField(widget=form.PasswordInput())
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def save(self, commit=True):
        user = User(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email']
        )
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        
        if password != password2:
            raise form.ValidationError('Passwords do not match')
        
        return cleaned_data
    
class UserLoginForm(form.Form):
    email = form.EmailField()
    password = form.CharField(widget=form.PasswordInput())
    class Meta:
        model = User
        fields = ['email', 'password']

    def get_user(self):
        print(User.objects.get(email=self.cleaned_data['email']))
        return User.objects.get(email=self.cleaned_data['email'])