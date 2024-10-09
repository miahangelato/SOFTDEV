from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("User must have an email address")
        if not username:
            raise ValueError("User must have a username")

        user = self.model(
            email=self.normalize_email(email),
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_staffuser(self, email, username, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

# Create your models here.
class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    @property
    def is_active(self):
        return self.active
    @property
    def is_staff(self):
        return self.staff
    @property
    def is_admin(self):
        return self.admin
    

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='seller_user')
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    shop_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField('products.Products', related_name='products', null=True, blank=True)
    orders = models.ManyToManyField('products.Order', related_name='orders', null=True, blank=True)
    reviews = models.ManyToManyField('products.Review', related_name='reviews', null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True, default='image/default.webp')

    def __str__(self):
        return str(self.user.email)

