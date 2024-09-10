from airflow.decorators import dag, task
from pendulum import datetime
from airflow.providers.apache.kafka.operators.produce import ProduceToTopicOperator
from airflow.providers.apache.kafka.operators.consume import ConsumeFromTopicOperator

import requests
import json
@dag(
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False
)
def stream_forex_data():

    @task
    def get_forex_data():
        # Fetch data from the API
        response = requests.get("https://financialmodelingprep.com/api/v3/fx?apikey=vtUz70wWFqQQ2B9cZGrnyfFLD61lDCXQ")
        # Ensure the response is successful
        response.raise_for_status()

        # Return the entire JSON response
        data = response.json()

        # Process each forex data item
        for item in data:
            print(f"Ticker: {item['ticker']}, Bid: {item['bid']}, Ask: {item['ask']}, Open: {item['open']}, Low: {item['low']}, High: {item['high']}, Changes: {item['changes']}, Date: {item['date']}")

        return data

    @task
    def format_data(raw_data):
        # Format the data into a readable string
        formatted_data = []
        for item in raw_data:
            formatted_item = (
                f"Ticker: {item.get('ticker', 'N/A')}, "
                f"Bid: {float(item['bid']) if item['bid'] is not None else 0.0:.5f}, "
                f"Ask: {float(item['ask']) if item['ask'] is not None else 0.0:.5f}, "
                f"Open: {float(item['open']) if item['open'] is not None else 0.0:.5f}, "
                f"Low: {float(item['low']) if item['low'] is not None else 0.0:.5f}, "
                f"High: {float(item['high']) if item['high'] is not None else 0.0:.5f}, "
                f"Changes: {float(item['changes']) if item['changes'] is not None else 0.0:.8f}, "
                f"Date: {item.get('date', 'N/A')}"
            )
            print(formatted_item)
            formatted_data.append(formatted_item)

        return formatted_data

    # Task to get forex data
    forex_data = get_forex_data()

    # Task to format forex data
    format_data(forex_data)

# Instantiate the DAG
stream_forex_data()