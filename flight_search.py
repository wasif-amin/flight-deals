import requests
from datetime import datetime
import os
from  dotenv import load_dotenv


load_dotenv()
TOKEN_URL = "https://test.api.amadeus.com/v1/security/oauth2/token"
IATA_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
FLIGHT_ENDPOINT = "https://test.api.amadeus.com/v2/shopping/flight-offers"
class FlightSearch:

    def __init__(self):
        self.api_key = os.environ["AMADEUS_API_KEY"]
        self.api_secret = os.environ["AMADEUS_API_SECRET"]
        self.token = self.get_new_token()

    def get_new_token(self):
        header = { "content-type": "application/x-www-form-urlencoded"}
        body = {
        "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.api_secret
        }
        response = requests.post(url=TOKEN_URL, headers=header, data=body)
        token = response.json()["access_token"]
        return token
    def get_destination_code(self, city_name):
        headers = {"Authorization": f"Bearer {self.token}"}
        query = {
        "keyword": city_name,
            "max": "2",
            "include": "AIRPORTS"
        }
        response = requests.get(url=IATA_ENDPOINT,headers=headers, params=query)
        print(f"status code: {response.status_code}, Airport IATA: {response.text}")
        try:
            code = response.json()["data"][0]["iataCode"]
        except IndexError:
            print(f"index error: no code found for{city_name}, bullshit. I know")


        return code

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):
        headers = {"Authorization": f"Bearer {self.token}"}
        query = {
            "originLocationCode": origin_city_code,
            "destinationLocationCode": destination_city_code,
            "departureDate": from_time.strftime("%Y-%m-%d"),
            "returnDate": to_time.strftime("%Y-%m-%d"),
            "adults": 1,
            "nonStop": "true",
            "currencyCode": "USD",
            "max": "10",
        }
        response = requests.get(url=FLIGHT_ENDPOINT, headers=headers, params=query)
        if response.status_code != 200:
            print(f"check_flights() response code: {response.status_code}")
            print("There was a problem with the flight search.\n"
                  "For details on status codes, check the API documentation:\n"
                  "https://developers.amadeus.com/self-service/category/flights/api-doc/flight-offers-search/api"
                  "-reference")
            print("Response body:", response.text)
            return None

        return response.json()



