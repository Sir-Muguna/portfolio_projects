import requests # type: ignore
from dotenv import load_dotenv # type: ignore
import os

# Load environment variables from .env file
load_dotenv()

# Access the secret variables
api_key = os.getenv("API_KEY")

# Build API URL with the actual key
api_url = f"http://api.weatherstack.com/current?access_key={api_key}&query=Nairobi"

def fetch_data():
    print("Fetching weather data from Weathrstack API...")
    try:
        response = requests.get(api_url)
        response.raise_for_status()  
        print("API response received successfully.")
        return response.json()

    except requests.exceptions.RequestException as e: 
        print(f"An error occurred: {e}")
        raise
    