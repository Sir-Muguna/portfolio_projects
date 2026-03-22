from kafka import KafkaConsumer
from json import loads, JSONDecodeError
from s3fs import S3FileSystem
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime
import os

# Load the .env file
load_dotenv()

# Get the Kafka bootstrap server from the environment variable
kafka_bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS")

if not kafka_bootstrap_servers:
    raise ValueError("KAFKA_BOOTSTRAP_SERVERS is not set in the .env file.")

def safe_json_deserializer(x):
    """Safely deserialize Kafka messages."""
    try:
        if not x:  # Check if the message is empty or None
            return None
        return loads(x.decode('utf-8'))
    except JSONDecodeError as e:
        print(f"Error decoding message: {e}")
        return None

def validate_data(data):
    """Validate the structure and format of the data."""
    try:
        # Validate date format
        datetime.strptime(data['date'], '%Y-%m-%d')  # Adjust format as needed
        # Ensure numeric fields are valid
        data['open'] = float(data['open'])
        data['high'] = float(data['high'])
        data['low'] = float(data['low'])
        data['close'] = float(data['close'])
        data['volume'] = int(data['volume'])
        return True
    except (ValueError, KeyError, TypeError) as e:
        print(f"Invalid data format: {e}")
        return False

def json_to_parquet(data, file_path):
    """Convert JSON data to Parquet format."""
    df = pd.DataFrame([data])  # Convert single record to a DataFrame
    df.to_parquet(file_path, engine='pyarrow', index=False)

try:
    # Initialize Kafka consumer
    consumer = KafkaConsumer(
        'stock_data',
        bootstrap_servers=[kafka_bootstrap_servers],
        auto_offset_reset='earliest',
        enable_auto_commit=False,  # Explicit commit for processed messages
        group_id='stock_data_group',
        value_deserializer=safe_json_deserializer
    )
    print("Consumer is connected and listening to the 'stock_data' topic...")
except Exception as e:
    print(f"Failed to connect to Kafka broker: {e}")
    raise

# Initialize S3 File System
s3 = S3FileSystem()

# Consume messages from the topic and send to S3
try:
    for count, message in enumerate(consumer):
        if message.value:  # Check if the message is not None
            data = message.value
            required_keys = {'symbol', 'date', 'open', 'high', 'low', 'close', 'volume'}
            if required_keys.issubset(data.keys()) and validate_data(data):
                # Partition data by date for Athena-compatible queries
                partition_date = data['date']
                s3_file_path = f"s3://stock-market-data-sirm/date={partition_date}/stock_ibm_data_{count}.parquet"
                print(f"Uploading validated data to S3: {s3_file_path}")
                
                # Write data in Parquet format to S3
                with s3.open(s3_file_path, 'wb') as file:
                    json_to_parquet(data, file)

                # Commit offset after successful processing
                consumer.commit()
            else:
                print(f"Received invalid or malformed data: {data}")
                with open('invalid_messages.log', 'a') as log_file:
                    log_file.write(f"{data}\n")
        else:
            print("Received an empty or invalid message.")
except KeyboardInterrupt:
    print("Consumer stopped by user.")
except Exception as e:
    print(f"An error occurred: {e}")
