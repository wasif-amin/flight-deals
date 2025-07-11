import  os
import requests
from  requests.auth import HTTPBasicAuth
from dotenv import load_dotenv


load_dotenv()

SHEETY_PRICES_ENDPOINT = "https://api.sheety.co/3b9cb90d1fadfb1ce66a24c0e971fc21/copyOfFlightDeals/prices/"

class DataManager:

    def __init__(self):
        self.user = os.getenv("SHEETY_USERNAME")
        self.password = os.getenv("SHEETY_PASSWORD")
        self.authorization = HTTPBasicAuth(self.user, self.password)
        self.destination_data = {}

    def get_destination_data(self):
        response = requests.get(url=SHEETY_PRICES_ENDPOINT, auth=self.authorization)
        print(response.request.headers)
        data = response.json()

        self.destination_data = data["prices"]


        return self.destination_data

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{SHEETY_PRICES_ENDPOINT}/{city['id']}",
                json=new_data,
                auth=self.authorization
            )
            print(response.text)
