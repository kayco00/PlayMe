import os
import requests
from dotenv import load_dotenv

load_dotenv()

TICKETMASTER_API_KEY = os.getenv("TICKETMASTER_API_KEY")
BASE_URL = "https://app.ticketmaster.com/discovery/v2/events.json"

def find_tour(artist_name:str)-> list[dict]:

    if not TICKETMASTER_API_KEY:
        print("Error with TICKETMASTER key")
        return[]

    params = {
        "apikey": TICKETMASTER_API_KEY,
        "keyword": artist_name,
        "classification": "Music",
        "size": 5,
        "sort": "date,asc"
    }

    response = requests.get(BASE_URL, params=params)
    if response.status_code != 200:
        return[]
    return response.json()

    