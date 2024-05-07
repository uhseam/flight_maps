from django.test import TestCase, RequestFactory
from .flight import Flight, get_airline_logo, get_hour, get_stoptime
from .booking import Booking, keep_date_remove_time
from .views import demo, book_flight, origin_airport_search, destination_airport_search, get_city_airport_list

# Create your tests here.

"""
To run coverage use the command while located in the flight_maps_api folder:
coverage run --source='.' manage.py test demo
(for windows: python -m coverage run --source='.' manage.py test demo) 

To see a report of the data after:
coverage report
(python -m coverage report for windows)
"""

#Flight Class Tests
class TestFlightMethods(TestCase):
    def setUp(self):
        # Initialize the Flight object with a sample flight dictionary
        self.flight_data = {
            'id': '123',
            'price': {'total': 100},
            'itineraries': [
                {
                    'segments': [
                        {
                            'departure': {'iataCode': 'JFK', 'at': '2024-05-03T08:00:00'},
                            'arrival': {'iataCode': 'LAX', 'at': '2024-05-03T11:00:00'},
                            'carrierCode': 'AA',
                            'duration': 'PT3H'
                        }
                    ],
                    'duration': 'PT3H'
                }
            ]
        }
        self.flight = Flight(self.flight_data)

    def test_construct_flights_one_stop(self):
        # Test for constructing flights with one stop
        offer = self.flight.construct_flights()
        # Assert statements for the constructed offer
        self.assertEqual(offer['price'], 100)
        self.assertEqual(offer['id'], '123')
        self.assertIn('0firstFlightDepartureAirport', offer)

    def test_construct_flights_direct_flight(self):
        # Test for constructing flights with direct flight
        self.flight_data['itineraries'][0]['segments'].append({
            'departure': {'iataCode': 'LAX', 'at': '2024-05-03T12:00:00'},
            'arrival': {'iataCode': 'JFK', 'at': '2024-05-03T15:00:00'},
            'carrierCode': 'AA',
            'duration': 'PT3H'
        })
        offer = self.flight.construct_flights()
        # Assert statements for the constructed offer
        self.assertEqual(offer['price'], 100)
        self.assertEqual(offer['id'], '123')
        self.assertIn('0firstFlightDepartureAirport', offer)
        self.assertIn('0stop_time', offer)


    def test_get_airline_logo(self):
        self.assertEqual(get_airline_logo('AA'), 'https://s1.apideeplink.com/images/airlines/AA.png')

    def test_get_hour(self):
        self.assertEqual(get_hour('2024-05-03T08:00:00'), '08:00')

    def test_get_stoptime(self):
        self.assertEqual(get_stoptime('PT6H', 'PT3H', 'PT3H'), '0:0')
    
    def test_construct_flights_missing_price(self):
        # Test for constructing flights with missing price
        self.flight_data.pop('price')
        self.assertRaises(ValueError, self.flight.construct_flights)

    def test_construct_flights_missing_itineraries(self):
        # Test for constructing flights with missing itineraries
        self.flight_data.pop('itineraries')
        self.assertRaises(ValueError, self.flight.construct_flights)

    def test_get_airline_logo_invalid_code(self):
        # Test for getting airline logo URL with invalid airline code
        self.assertRaises(ValueError, get_airline_logo, 'XYZ')

    def test_get_hour_invalid_format(self):
        # Test for getting hour with invalid datetime format
        self.assertRaises(ValueError, get_hour, '2024-05-03')

    def test_get_stoptime_invalid_duration_format(self):
        # Test for calculating stop time with invalid duration format
        self.assertRaises(ValueError, get_stoptime, '6 hours', '3 hours', '3 hours')


#Booking Class Tests
class TestBookingMethods(TestCase):

    def setUp(self):
        # Initialize the Booking object with a sample flight dictionary
        self.booking_data = {
            'flightOffers': [
                {
                    'price': {'total': 200},
                    'itineraries': [
                        {
                            'segments': [
                                {
                                    'departure': {'iataCode': 'JFK', 'at': '2024-05-03T08:00:00'},
                                    'arrival': {'iataCode': 'LAX', 'at': '2024-05-03T11:00:00'},
                                    'carrierCode': 'AA',
                                    'duration': 'PT3H'
                                }
                            ]
                        }
                    ]
                }
            ],
            'associatedRecords': [
                {'creationDate': '2024-05-03T12:00:00', 'reference': 'ABC123'}
            ],
            'ticketingAgreement': {'option': 'confirmed'},
            'travelers': [
                {'name': {'firstName': 'John', 'lastName': 'Doe'}}
            ]
        }
        self.booking = Booking(self.booking_data)

    def test_construct_booking_one_stop(self):
        # Test for constructing booking with one stop
        offer = self.booking.construct_booking()
        # Assert statements for the constructed offer
        self.assertEqual(offer['price'], 200)
        self.assertIn('created', offer)

    def test_construct_booking_direct_flight(self):
        # Test for constructing booking with direct flight
        offer = self.booking.construct_booking()
        # Assert statements for the constructed offer
        self.assertEqual(offer['price'], 200)
        self.assertIn('created', offer)
        self.assertEqual(offer['reference'], 'ABC123')
        self.assertEqual(offer['confirmed'], 'confirmed')
        self.assertEqual(offer['first_name'], 'John')
        self.assertEqual(offer['last_name'], 'Doe')
        self.assertIn('0firstFlightDepartureAirport', offer)
    
    def test_keep_date_remove_time(self):
        # Sample datetime string with time
        datetime_with_time = '2024-05-03T12:00:00'
        
        # Call the function
        result = keep_date_remove_time(datetime_with_time)
        
        # Assert that the time portion is removed
        self.assertEqual(result, '2024-05-03')

    def test_construct_booking_missing_price(self):
        # Test for constructing booking with missing price
        self.booking_data['flightOffers'][0].pop('price')
        self.assertRaises(ValueError, self.booking.construct_booking)
        
    def test_construct_booking_missing_traveler_name(self):
        # Test for constructing booking with missing traveler name
        self.booking_data['travelers'][0].pop('name')
        self.assertRaises(ValueError, self.booking.construct_booking)
        
    def test_construct_booking_missing_reference(self):
        # Test for constructing booking with missing reference
        self.booking_data['associatedRecords'][0].pop('reference')
        self.assertRaises(ValueError, self.booking.construct_booking)
        
    def test_keep_date_remove_time_invalid_format(self):
        # Test for invalid datetime format
        datetime_with_time = '2024-05-03'
        self.assertRaises(ValueError, keep_date_remove_time, datetime_with_time)




class TestViewMethods(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_demo(self): # pragma: no cover
        
        # Create instance of get request
        request = self.factory.get('')
        # Test demo view
        response = demo(request)
        self.assertEqual(response.status_code, 200)

    def test_book_flight(self):
        # Create instance of get request
        request = self.factory.get('book_flight/<str:flight>/')

        # Test demo view
        response = book_flight(request, self.flight)
        self.assertEqual(response.status_code, 200)

    def test_origin_airport_search(self): # pragma: no cover
        request = self.factory.get('')

        response = origin_airport_search(request, self.flight)
        self.assertEqual(response.status_code, 200)

    def test_destination_airport_search(self): # pragma: no cover
        #Create request
        request = self.factory.get('destination_airport_search/')

        #test destination search view
        response = destination_airport_search(request, self.flight)
        self.assertEqual(response.status_code, 200)

    def test_get_city_airport_list(self): # pragma: no cover
        #Create request
        request = self.factory.get('destination_airport_search/')

        #test destination search view
        response = destination_airport_search(request, self.flight)
        self.assertEqual(response.status_code, 200)
        
    #false tests
    
    def test_demo_err(self): # pragma: no cover
        
        # Create instance of get request
        request = self.factory.get('')
        # Test demo view
        response = demo(request)
        self.assertEqual(response.status_code, 400)

    def test_book_flight_err(self):
        # Create instance of get request
        request = self.factory.get('book_flight/<str:flight>/')

        # Test demo view
        response = book_flight(request, self.flight)
        self.assertEqual(response.status_code, 400)

    def test_origin_airport_search_err(self): # pragma: no cover
        request = self.factory.get('')

        response = origin_airport_search(request, self.flight)
        self.assertEqual(response.status_code, 400)

    def test_destination_airport_search_err(self): # pragma: no cover
        #Create request
        request = self.factory.get('destination_airport_search/')

        #test destination search view
        response = destination_airport_search_err(request, self.flight)
        self.assertEqual(response.status_code, 400)

    def test_get_city_airport_list_err(self): # pragma: no cover
        #Create request
        request = self.factory.get('destination_airport_search/')

        #test destination search view
        response = destination_airport_search(request, self.flight)
        self.assertEqual(response.status_code, 400)
