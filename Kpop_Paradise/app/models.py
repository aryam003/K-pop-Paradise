from django.db import models
from django.contrib.auth.models import User

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
    
    def _str_(self):
        return f"{self.band.name} - {self.location} on {self.date}"


class Ticket(models.Model):
    concert = models.ForeignKey(Concert, on_delete=models.CASCADE, related_name="tickets")
    buyer_name = models.CharField(max_length=100)
    email = models.EmailField()
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2 ,null=True, blank=True)  
   


    def _str_(self):
        return f"{self.buyer_name} - {self.concert.band.name}"
    
    
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
    email = models.EmailField()

 