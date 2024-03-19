import requests
from typing import List
from .models import Flight, Reservation
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.conf import settings
from django.contrib.auth import get_user_model
from flight_maps_app.models import UserProfile

class FlightSearch:
    @staticmethod
    def find_flights(source: str, destination: str, date: str) -> List[Flight]:
        """
        Search for flights from source to destination on a specific date.
        Parameters:
        - source (str): The departure location.
        - destination (str): The arrival location.
        - date (str): The date of travel in YYYY-MM-DD format.
        Returns:
        - list[Flight]: A list of Flight objects that match the search criteria.
        """
        # Placeholder: In a real scenario, fetch flights from database
        flights = [
            Flight("CityA", "CityB", "2024-01-01", 100, 120, 0),
            Flight("CityA", "CityB", "2024-01-01", 150, 110, 1),
            # Add more flights for testing
        ]
        return [flight for flight in flights if flight.source == source and flight.destination == destination and flight.date == date]

    @staticmethod
    def filter_flights_by_price(flights: List[Flight], max_price: float) -> List[Flight]:
        """
        Filters flights by maximum price.
        Parameters:
        - flights (list[Flight]): The list of flights to filter.
        - max_price (float): The maximum price for the flight.
        Returns:
        - list[Flight]: A list of Flight objects that are below the maximum price.
        """
        return [flight for flight in flights if flight.price <= max_price]

    @staticmethod
    def filter_flights_by_duration(flights: List[Flight], max_duration: int) -> List[Flight]:
        """
        Filters flights by maximum duration.
        Parameters:
        - flights (list[Flight]): The list of flights to filter.
        - max_duration (int): The maximum duration for the flight in minutes.
        Returns:
        - list[Flight]: A list of Flight objects that have a duration less than or equal to the maximum duration.
        """
        return [flight for flight in flights if flight.duration <= max_duration]

    @staticmethod
    def filter_flights_by_stops(flights: List[Flight], max_stops: int) -> List[Flight]:
        """
        Filters flights by the maximum number of stops.
        Parameters:
        - flights (list[Flight]): The list of flights to filter.
        - max_stops (int): The maximum number of stops for the flight.
        Returns:
        - list[Flight]: A list of Flight objects that have a number of stops less than or equal to the maximum number of stops.
        """
        return [flight for flight in flights if flight.stops <= max_stops]

class FlightReservation:
    # Assuming a simple in-memory store for demonstration purposes
    reservations = {}
    next_reservation_id = 1

    @staticmethod
    def select_flight(flight_id: int) -> bool:
        """
        Selects a flight for booking. This method can be expanded to validate 
        flight availability or any other pre-reservation checks.
        Parameters:
        - flight_id (int): The ID of the flight to be selected for booking.
        Returns:
        - bool: True if the flight is available for booking, False otherwise.
        """
        # Placeholder for actual flight selection logic
        return True

    @classmethod
    def reserve_flight(cls, flight_id: int, user_id: int) -> int:
        """
        Reserves the selected flight for the user and returns a reservation ID.
        Parameters:
        - flight_id (int): The ID of the flight to be reserved.
        - user_id (int): The ID of the user making the reservation.
        Returns:
        - int: The reservation ID of the newly created reservation.
        """
        if cls.select_flight(flight_id):
            reservation_id = cls.next_reservation_id
            cls.reservations[reservation_id] = Reservation(reservation_id, flight_id, user_id)
            cls.next_reservation_id += 1
            return reservation_id
        else:
            raise ValueError("Flight selection failed. Reservation could not be completed.")

    @classmethod
    def cancel_reservation(cls, reservation_id: int) -> bool:
        """
        Cancels an existing flight reservation.
        Parameters:
        - reservation_id (int): The ID of the reservation to cancel.
        Returns:
        - bool: True if the reservation was successfully cancelled, False otherwise.
        """
        reservation = cls.reservations.get(reservation_id)
        if reservation and reservation.is_active:
            reservation.is_active = False
            return True
        else:
            return False

User = get_user_model()

class UserAccount:
    @classmethod
    def create_account(cls, email: str, password: str, user_identifier: str):
        """
        Creates a new user account with the given email, password, and user identifier.
        Parameters:
        - email (str): The email address for the new account.
        - password (str): The password for the new account.
        - user_identifier (str): A unique identifier for the user.
        Returns:
        - user: The User instance that was created.
        Raises:
        - ValueError: If an account with this email already exists.
        """
        try:
            user = User.objects.create_user(username=email, email=email, password=password)
            UserProfile.objects.create(user=user, user_identifier=user_identifier)
            return user
        except IntegrityError:
            raise ValueError("An account with this email already exists.")

    @classmethod
    def login_user(cls, request, email: str, password: str):
        """
        Authenticates a user based on an email and password.
        Parameters:
        - request: HttpRequest object from Django.
        - email (str): The email address of the user.
        - password (str): The password of the user.
        Returns:
        - bool: True if login is successful, False otherwise.
        """
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return True
        else:
            return False

    @classmethod
    def logout_user(cls, request):
        """
        Logs out the user.
        Parameters:
        - request: HttpRequest object from Django.
        """
        logout(request)

