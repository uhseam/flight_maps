import pytest
from .services import fetch_booking_url
from unittest.mock import patch

@patch('requests.get')
def test_fetch_booking_url(mock_get):
    # Setup mock
    mock_response = {
        "success": True,
        "data": {
            "url": "https://example.com/booking"
        }
    }
    mock_get.return_value = mock_response
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response
    
    # Call the function
    result = fetch_booking_url('hash', 'dest', 'id', 'orig', 'searchid')
    
    # Asserts
    mock_get.assert_called_once_with(
        "https://travel-advisor.p.rapidapi.com/flights/get-booking-url",
        headers={
            "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
            "X-RapidAPI-Host": "travel-advisor.p.rapidapi.com"
        },
        params={
            "searchHash": 'hash',
            "Dest": 'dest',
            "id": 'id',
            "Orig": 'orig',
            "searchId": 'searchid'
        }
    )
    assert result == mock_response
    assert 'url' in result['data']

# Additional test to simulate network failures and bad responses
@patch('requests.get')
def test_fetch_booking_url_failure(mock_get):
    mock_get.return_value.status_code = 500
    with pytest.raises(Exception):
        fetch_booking_url('hash', 'dest', 'id', 'orig', 'searchid')
