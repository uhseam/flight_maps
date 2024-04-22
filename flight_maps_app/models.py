from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from datetime import date


# Create your models here.
'''
class Flight(models.Model):
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField()  # duration in minutes
    stops = models.IntegerField()

    def __str__(self):
        return f"{self.source} to {self.destination} on {self.date}"
#might remove
'''
'''
class Reservation(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    #user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Reservation {self.id} for Flight {self.flight_id} by User {self.user_id}"
'''


'''
class UserProfile(models.Model):
    user = models.OneToOneField(
        #settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='userprofile'
    )
    user_identifier = models.CharField(max_length=100, unique=True)
'''

class Flight(models.Model):
    flight_id = models.CharField(max_length=20, primary_key=True)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    duration = models.IntegerField(help_text="Duration in minutes")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    number_of_stops = models.IntegerField()
    """
    booking_url = models.URLField(
        _("Booking URL"), 
        max_length=128, 
        db_index=True, 
        unique=True, 
        blank=True
    )
    """

    def __str__(self):
        return f"Flight {self.flight_id} from {self.source} to {self.destination}"