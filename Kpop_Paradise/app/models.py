from django.db import models
from django.contrib.auth.models import User
from .constants import PaymentStatus
from django.db.models.fields import CharField
from django.utils.translation import gettext_lazy as _
# Create your models here.

class Band(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='bands/', null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class Concert(models.Model):
    band = models.ForeignKey(Band, on_delete=models.CASCADE, related_name="concerts")
    artist = models.CharField(max_length=100)
    date = models.DateField()
    location = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='bands/', null=True, blank=True)
    total_ticket = models.PositiveIntegerField(default=100)
    
    def __str__(self):
        return f"{self.band.name} - {self.location} on {self.date}"

class Ticket(models.Model):
    concert = models.ForeignKey(Concert, on_delete=models.CASCADE, related_name="tickets")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    buyer_name = models.CharField(max_length=100)
    email = models.EmailField()
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)  # New field



class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # In your Order model, temporarily allow nulls for the concert field
    concert = models.ForeignKey(Concert, on_delete=models.CASCADE, related_name="orders", null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Changed to DecimalField
    status = models.CharField(
        _("Payment Status"),
        default=PaymentStatus.PENDING,
        max_length=254,
        blank=False,
        null=False
    )
    provider_order_id = models.CharField(_("Order ID"), max_length=40, null=False, blank=False)
    payment_id = models.CharField(_("Payment ID"), max_length=36, null=False, blank=False)
    signature_id = models.CharField(_("Signature ID"), max_length=128, null=False, blank=False)

    def __str__(self):
        return f"{self.user.username} - {self.provider_order_id}"

class Buy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    concert = models.ForeignKey(Concert, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_confirmed = models.BooleanField(default=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)

 








#-------PRODUCTS-----------------------------------------------------------------------------------------------------------

class products(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True)
    band = models.ForeignKey(Band, on_delete=models.CASCADE)



    

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} in {self.user.username}'s cart"

class Booking(models.Model):
    product = models.ForeignKey(products, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Assuming the user is logged in
    booking_date = models.DateTimeField(auto_now_add=True)
    buyer_name = models.CharField(max_length=100)
    address = models.TextField(null=True, blank=True)
    email = models.EmailField()
    price = models.DecimalField(max_digits=10, decimal_places=2 ,default=0.00) 


class Order2(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
   
    product = models.ForeignKey(products, on_delete=models.CASCADE, related_name="orders", null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Changed to DecimalField
    status = models.CharField(
        _("Payment Status"),
        default=PaymentStatus.PENDING,
        max_length=254,
        blank=False,
        null=False
    )
    provider_order_id = models.CharField(_("Order ID"), max_length=40, null=False, blank=False)
    payment_id = models.CharField(_("Payment ID"), max_length=36, null=False, blank=False)
    signature_id = models.CharField(_("Signature ID"), max_length=128, null=False, blank=False)

    def __str__(self):
        return f"{self.user.username} - {self.provider_order_id}"

class Buy2(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(products, on_delete=models.CASCADE)
    buyer_name = models.CharField(max_length=100)
    address = models.TextField(Booking,null=True, blank=True)
    email = models.EmailField()
    price = models.DecimalField(max_digits=10, decimal_places=2 ,default=0.00)   
    is_confirmed = models.BooleanField(default=False)
    order = models.ForeignKey(Order2, on_delete=models.CASCADE, null=True)








class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    name = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username 
    

      