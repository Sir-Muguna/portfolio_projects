import pandas as pd
from kafka import KafkaProducer
from time import sleep
import requests
from dotenv import load_dotenv
import os
import json

# Load the .env file
load_dotenv()

# Get the API key and Kafka bootstrap servers from environment variables
alpha_vantage_api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
kafka_bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS")

# Validate environment variables
if not alpha_vantage_api_key:
    raise ValueError("API key for Alpha Vantage is missing. Set ALPHA_VANTAGE_API_KEY in your .env file.")
if not kafka_bootstrap_servers:
    raise ValueError("Kafka bootstrap servers are missing. Set KAFKA_BOOTSTRAP_SERVERS in your .env file.")

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers=[kafka_bootstrap_servers],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')  # Serialize dictionary to JSON bytes
)

# Define the stock symbol and the Alpha Vantage API endpoint
symbol = "IBM"  # Replace with the stock symbol of your choice
url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={alpha_vantage_api_key}'

# Fetch stock data and send it to the Kafka topic
try:
    while True:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            # Check if the API response contains "Time Series (Daily)"
            if "Time Series (Daily)" in data:
                for date, stats in data["Time Series (Daily)"].items():
                    message = {
                        "symbol": symbol,
                        "date": date,
                        "open": stats["1. open"],
                        "high": stats["2. high"],
                        "low": stats["3. low"],
                        "close": stats["4. close"],
                        "volume": stats["5. volume"]
                    }
                    # Send message to Kafka topic
                    producer.send('stock_data', value=message)
                    print(f"Sent: {message}")
                    sleep(1)  # Simulate real-time streaming
            else:
                print("Error: 'Time Series (Daily)' not found in API response")
        else:
            print(f"Error: Failed to fetch data. Status code: {response.status_code}")
        
        # Wait for 60 seconds before the next API call
        sleep(60)
except KeyboardInterrupt:
    print("Stopped by user")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    producer.close()
