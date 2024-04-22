import requests
import os

def get_booking_url(search_hash, dest, id, orig, search_id):
    api_key = os.getenv('RAPIDAPI_KEY')
    if not api_key:
        raise Exception("API key not found. Please set the RAPIDAPI_KEY environment variable.")

    url = "https://travel-advisor.p.rapidapi.com/flights/get-booking-url"
    querystring = {
        "searchHash": search_hash,
        "Dest": dest,
        "id": id,
        "Orig": orig,
        "searchId": search_id
    }

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "travel-advisor.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")
