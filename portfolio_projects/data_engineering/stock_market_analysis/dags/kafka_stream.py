from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
# from airflow.hooks.base_hook import BaseHook  # Manage connections via BaseHook
import requests
import json
from kafka import KafkaProducer
import logging
import time

# Manage connections and credentials for external services in Airflow.
# connection = BaseHook.get_connection("financial_api")
# api_key = connection.password

# Default arguments for the DAG
default_args = {
    'owner': 'sirmuguna',
    'start_date': datetime(2024, 9, 1),
    'retries': 3,  # Retries on failure
    'retry_delay': timedelta(minutes=5),  # Retry after 5 mins
}

# Create the DAG object
dag = DAG(
    'stream_forex_data',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
)

# Extract logic into functions for easy testing
def fetch_forex_data(**kwargs):
    try:
        response = requests.get(
            f"https://financialmodelingprep.com/api/v3/fx?apikey=vtUz70wWFqQQ2B9cZGrnyfFLD61lDCXQ", 
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        logging.info(f"Fetched Forex Data: {data}")

        # Push data to XCom for other tasks to use
        kwargs['ti'].xcom_push(key='forex_data', value=data)
        return data
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching forex data: {e}")
        raise

def process_forex_data(**kwargs):
    raw_data = kwargs['ti'].xcom_pull(task_ids='fetch_forex_data', key='forex_data')
    
    formatted_data = []
    for item in raw_data:
        formatted_item = {
            "ticker": item.get('ticker', 'N/A'),
            "bid": round(float(item['bid']) if item['bid'] is not None else 0.0, 5),
            "ask": round(float(item['ask']) if item['ask'] is not None else 0.0, 5),
            "open": round(float(item['open']) if item['open'] is not None else 0.0, 5),
            "low": round(float(item['low']) if item['low'] is not None else 0.0, 5),
            "high": round(float(item['high']) if item['high'] is not None else 0.0, 5),
            "changes": round(float(item['changes']) if item['changes'] is not None else 0.0, 8),
            "date": item.get('date', 'N/A')
        }
        formatted_data.append(formatted_item)
        logging.info(f"Processed item: {formatted_item}")

    # Push formatted data to XCom for the next task
    kwargs['ti'].xcom_push(key='formatted_data', value=formatted_data)
    return formatted_data

def stream_data(**kwargs):
    formatted_data = kwargs['ti'].xcom_pull(task_ids='process_forex_data', key='formatted_data')
    
    producer = None
    try:
        producer = KafkaProducer(bootstrap_servers=['broker:29092'], max_block_ms=5000)
        logging.info("Kafka producer created successfully.")
    except Exception as e:
        logging.error(f"Failed to connect to Kafka: {e}")
        raise
    
    curr_time = time.time()
    while time.time() < curr_time + 60:  # Stream for 1 minute
        try:
            # Send formatted data to Kafka
            producer.send('forex_data', json.dumps(formatted_data).encode('utf-8'))
            producer.flush()
            logging.info("Data sent to Kafka.")
        except Exception as e:
            logging.error(f"Error sending data to Kafka: {e}")
            time.sleep(5)  # Pause before retrying to avoid overloading Kafka
    
    if producer:
        producer.close()

# Define the tasks
fetch_task = PythonOperator(
    task_id='fetch_forex_data',
    python_callable=fetch_forex_data,
    dag=dag
)

process_task = PythonOperator(
    task_id='process_forex_data',
    python_callable=process_forex_data,
    dag=dag
)

stream_task = PythonOperator(
    task_id='stream_data_from_api',
    python_callable=stream_data,
    dag=dag
)

# Define the task dependencies
fetch_task >> process_task >> stream_task
