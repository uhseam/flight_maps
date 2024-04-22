"""
To run coverage use the command while located in the flight_maps folder:
coverage run --source='.' manage.py test flight_maps_app
(for windows: python -m coverage run --source='.' manage.py test flight_maps_app) 

To see a report of the data after:
coverage report
(python -m for windows)
"""

from django.test import TestCase
from .models import Flight#, FlightReservation, Reservation, UserAccount, User
from .utils import FlightSearch#, Flight
from django.utils import timezone
from datetime import timedelta
from datetime import datetime
#from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

# Create your tests here.

class FlightSearchTestCase(TestCase):
    def setUp(self):
        # Setup sample flights for testing
        self.flight1 = Flight.objects.create(flight_id="1", source="NYC", destination="LAX", departure_time=timezone.datetime(2024, 1, 1), arrival_time=timezone.datetime(2024, 1, 1, 5), duration=300, price=200, number_of_stops=0)
        self.flight2 = Flight.objects.create(flight_id="2", source="NYC", destination="LAX", departure_time=timezone.datetime(2024, 1, 1), arrival_time=timezone.datetime(2024, 1, 1, 4, 40), duration=280, price=150, number_of_stops=1)
        self.flight3 = Flight.objects.create(flight_id="3", source="NYC", destination="LAX", departure_time=timezone.datetime(2024, 1, 2), arrival_time=timezone.datetime(2024, 1, 2, 6), duration=360, price=100, number_of_stops=2)
        self.flight4 = Flight.objects.create(flight_id="4", source="NYC", destination="LAX", departure_time=timezone.datetime(2024, 1, 1), arrival_time=timezone.datetime(2024, 1, 1, 4, 30), duration=270, price=250, number_of_stops=0)

    def test_find_flights_on_specific_date(self):
        """Test that find_flights returns flights on a specific date."""
        flights = FlightSearch.find_flights("NYC", "LAX", timezone.datetime(2024, 1, 1).date())
        self.assertEqual(len(flights), 3, "Should find 3 flights on 2024-01-01")

    def test_filter_flights_by_price(self):
        """Test that filter_flights_by_price returns flights below a maximum price."""
        flights = Flight.objects.all()
        filtered_flights = FlightSearch.filter_flights_by_price(flights, 200)
        self.assertEqual(len(filtered_flights), 2, "Should find 2 flights below $200")

    def test_filter_flights_by_duration(self):
        """Test that filter_flights_by_duration returns flights with duration below a maximum."""
        flights = Flight.objects.all()
        filtered_flights = FlightSearch.filter_flights_by_duration(flights, 300)
        self.assertEqual(len(filtered_flights), 3, "Should find 3 flights with duration below 300 minutes")

    def test_filter_flights_by_stops(self):
        """Test that filter_flights_by_stops returns flights with stops below a maximum number."""
        flights = Flight.objects.all()
        filtered_flights = FlightSearch.filter_flights_by_stops(flights, 1)
        self.assertEqual(len(filtered_flights), 3, "Should find 3 flights with 1 or fewer stops")

    def test_find_flights_returns_empty_list_for_no_match(self):
        """Test that find_flights returns an empty list when no flights match the criteria."""
        flights = FlightSearch.find_flights("NYC", "LAX", timezone.datetime(2024, 1, 3).date())
        self.assertEqual(len(flights), 0, "Should return an empty list when no flights match the criteria")

'''
class FlightReservationTestCase(TestCase):
    def setUp(self):
        # Reset or initialize the FlightReservation system as needed
        # Create sample flights and users if your implementation requires them
        Flight.objects.create(flight_id="1", source="NYC", destination="LAX",)
        #self.user = User.objects.create_user(username='testuser', password='12345')
        FlightReservation.reservations = {}
        FlightReservation.next_reservation_id = 1

    def test_select_flight(self):
        """Test that select_flight method returns True indicating the flight can be selected."""
        self.assertTrue(FlightReservation.select_flight(flight_id="1"), "Flight selection should be possible")

    def test_reserve_flight_success(self):
        """Test that reserve_flight successfully reserves a flight and returns a reservation ID."""
        reservation_id = FlightReservation.reserve_flight(flight_id="1", user_id=self.user.id)
        self.assertEqual(reservation_id, 1, "Reservation ID should be 1 for the first reservation")
        reservation = FlightReservation.reservations.get(reservation_id)
        self.assertIsNotNone(reservation, "Reservation should exist")
        self.assertEqual(reservation.user_id, self.user.id, "User ID should match the reservation")

    def test_reserve_flight_invalid_selection(self):
        """Test reserve_flight with an invalid selection, expecting a ValueError."""
        with self.assertRaises(ValueError):
            FlightReservation.reserve_flight(flight_id="999", user_id=self.user.id)

    def test_cancel_reservation_success(self):
        """Test that cancel_reservation successfully cancels an existing reservation."""
        reservation_id = FlightReservation.reserve_flight(flight_id="1", user_id=self.user.id)
        result = FlightReservation.cancel_reservation(reservation_id)
        self.assertTrue(result, "Canceling the reservation should succeed")
        reservation = FlightReservation.reservations.get(reservation_id)
        self.assertFalse(reservation.is_active, "Reservation should be marked as inactive")

    def test_cancel_reservation_invalid_id(self):
        """Test cancel_reservation with an invalid reservation_id, expecting False."""
        result = FlightReservation.cancel_reservation(reservation_id=999)
        self.assertFalse(result, "Canceling with an invalid ID should fail")
'''

#User = get_user_model()
'''
class UserAccountTestCase(TestCase):
    def test_create_account_success(self):
        """
        Test that creating a new user account successfully returns a new user instance.
        """
        email = "test@example.com"
        password = "password123"
        user = User.objects.create_user(email=email, password=password)
        self.assertEqual(user.email, email, "Should successfully create a new user and return user instance")

    def test_create_account_duplicate_email(self):
        """
        Test creating a user account with a duplicate email raises an error.
        """
        email = "test@example.com"
        password = "password123"
        User.objects.create_user(email=email, password=password)
        with self.assertRaises(ValidationError):
            User.objects.create_user(email=email, password="newpassword123")

    def test_login_success(self):
        """
        Test that a user can log in with correct credentials.
        """
        email = "login_success@example.com"
        password = "password123"
        User.objects.create_user(username=email, email=email, password=password)
        logged_in = self.client.login(username=email, password=password)
        self.assertTrue(logged_in, "Login should succeed with correct credentials")

    def test_login_failure(self):
        """
        Test that a user cannot log in with incorrect credentials.
        """
        email = "login_failure@example.com"
        password = "password123"
        User.objects.create_user(username=email, email=email, password=password)
        logged_in = self.client.login(username=email, password="wrongpassword")
        self.assertFalse(logged_in, "Login should fail with incorrect credentials")

    def test_logout(self):
        """
        Test that a user is logged out successfully.
        """
        email = "logout_test@example.com"
        password = "password123"
        User.objects.create_user(username=email, email=email, password=password)
        self.client.login(username=email, password=password)
        self.client.logout()
        # To test logout, you can check if the client's session was cleared.
        self.assertNotIn('_auth_user_id', self.client.session, "User should be logged out and session cleared")
'''