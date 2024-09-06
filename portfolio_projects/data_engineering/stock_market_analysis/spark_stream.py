import logging
from cassandra.cluster import Cluster
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, FloatType, TimestampType
from pyspark.sql.functions import from_json, col
import uuid

# Create keyspace if it doesn't exist
def create_keyspace(session):
    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS spark_streams
        WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'};
    """)
    logging.info("Keyspace 'spark_streams' created successfully!")


# Create the forex_table table if it doesn't exist
def create_table(session):
    session.execute("""
    CREATE TABLE IF NOT EXISTS spark_streams.forex_table (
        id UUID PRIMARY KEY,
        ticker TEXT,
        bid FLOAT,
        ask FLOAT,
        open_price FLOAT, 
        low FLOAT,
        high FLOAT,
        changes FLOAT,
        date TIMESTAMP
    );
    """)
    logging.info("Table 'forex_table' created successfully!")


# Insert data into Cassandra
def insert_data(session, **kwargs):
    logging.info("Inserting data...")

    ticker_id = uuid.uuid4()  # Generates a new UUID
    ticker_name = kwargs.get('ticker')
    bid = kwargs.get('bid')
    ask = kwargs.get('ask')
    open_price = kwargs.get('open') 
    low = kwargs.get('low')
    high = kwargs.get('high')
    changes = kwargs.get('changes')
    date = kwargs.get('date')

    try:
        session.execute("""
            INSERT INTO spark_streams.forex_table (id, ticker, bid, ask, open_price, low, high, changes, date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (ticker_id, ticker_name, bid, ask, open_price, low, high, changes, date))
        logging.info(f"Data inserted for {ticker_name} with bid {bid}")

    except Exception as e:
        logging.error(f"Could not insert data due to: {e}")


# Create Spark session
def create_spark_connection():
    try:
        spark_conn = SparkSession.builder \
            .appName('SparkDataStreaming') \
            .config('spark.jars.packages', "com.datastax.spark:spark-cassandra-connector_2.13:3.4.1,"
                                           "org.apache.spark:spark-sql-kafka-0-10_2.13:3.4.1") \
            .config('spark.cassandra.connection.host', 'localhost') \
            .getOrCreate()

        spark_conn.sparkContext.setLogLevel("ERROR")
        logging.info("Spark connection created successfully!")
        return spark_conn
    except Exception as e:
        logging.error(f"Couldn't create the Spark session due to: {e}")
        return None


# Connect to Kafka topic
def connect_to_kafka(spark_conn):
    try:
        spark_df = spark_conn.readStream \
            .format('kafka') \
            .option('kafka.bootstrap.servers', 'localhost:9092') \
            .option('subscribe', 'forex_data') \
            .option('startingOffsets', 'earliest') \
            .load()
        logging.info("Kafka dataframe created successfully.")
        return spark_df
    except Exception as e:
        logging.error(f"Kafka dataframe could not be created due to: {e}")
        return None


# Create Cassandra connection
def create_cassandra_connection():
    try:
        cluster = Cluster(['localhost'])
        session = cluster.connect()
        logging.info("Connected to Cassandra cluster.")
        return session
    except Exception as e:
        logging.error(f"Could not create Cassandra connection due to: {e}")
        return None


# Select relevant fields from Kafka stream
def create_selection_df_from_kafka(spark_df):
    schema = StructType([
        StructField("ticker", StringType(), False),
        StructField("bid", FloatType(), False),
        StructField("ask", FloatType(), False),
        StructField("open", FloatType(), False),
        StructField("low", FloatType(), False),
        StructField("high", FloatType(), False),
        StructField("changes", FloatType(), False),
        StructField("date", TimestampType(), False) 
    ])

    try:
        # Cast Kafka value to string and apply schema
        sel = spark_df.selectExpr("CAST(value AS STRING)") \
            .select(from_json(col('value'), schema).alias('data')).select("data.*")
        
        logging.info("Schema successfully applied to Kafka stream.")
        return sel

    except Exception as e:
        logging.error(f"Error applying schema to Kafka stream: {e}")
        return None


if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(level=logging.INFO)

    # Create Spark connection
    spark_conn = create_spark_connection()

    if spark_conn:
        # Connect to Kafka and get data stream
        spark_df = connect_to_kafka(spark_conn)
        if spark_df:
            selection_df = create_selection_df_from_kafka(spark_df)
            session = create_cassandra_connection()

            if session:
                create_keyspace(session)
                create_table(session)

                logging.info("Starting the streaming process...")

                # Write data to Cassandra
                streaming_query = (selection_df.writeStream
                                   .format("org.apache.spark.sql.cassandra")
                                   .option('checkpointLocation', '/tmp/checkpoint')
                                   .option('keyspace', 'spark_streams')
                                   .option('table', 'forex_table')
                                   .start())

                # Await termination
                streaming_query.awaitTermination()
