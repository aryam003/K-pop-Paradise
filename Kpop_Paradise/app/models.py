from django.db import models

# Create your models here.

class Band(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='bands/', null=True, blank=True)
    description = models.TextField()

    def _str_(self):
        return self.name

class Concert(models.Model):
    band = models.ForeignKey(Band, on_delete=models.CASCADE, related_name="concerts")
    artist = models.CharField(max_length=100)
    date = models.DateField()
    location = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    total_ticket = models.PositiveIntegerField(default=100)
    
    # def available_tickets(self):
    #     booking_tickets=sum(ticket.quantity for in self)

    def _str_(self):
        return f"{self.band.name} - {self.location} on {self.date}"

# CATEGORY_CHOICES=[
#     ('VIP','VIP'),
#     ('regular','regular')
# ]
    

class Ticket(models.Model):
    concert = models.ForeignKey(Concert, on_delete=models.CASCADE, related_name="tickets")
    buyer_name = models.CharField(max_length=100)
    email = models.EmailField()
    quantity = models.PositiveIntegerField()

    def _str_(self):
        return f"{self.buyer_name} - {self.concert.band.name}"
    