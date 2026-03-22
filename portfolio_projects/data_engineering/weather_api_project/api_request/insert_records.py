from api_request import fetch_data # type: ignore   
from datetime import datetime                       
import psycopg2 # type: ignore                     


def connect_to_db():
    print("Connecting to PostgreSQL database...")
    try:
        # Establish connection to PostgreSQL using provided credentials
        conn = psycopg2.connect(
            host="db",
            port=5432,
            dbname="db",
            user="db_user",
            password="db_password"
        )
        return conn 
    except psycopg2.Error as e:
        print(f"Database connection failed: {e}")
        raise
    
def create_table(conn):
    print("Creating table if not exists...")
    try:
        cursor = conn.cursor()
        # Create schema and table if they don’t already exist
        cursor.execute("""
             CREATE SCHEMA IF NOT EXISTS dev;
             CREATE TABLE IF NOT EXISTS dev.raw_weather_data(
                 id SERIAL PRIMARY KEY,
                 city TEXT,
                 temperature FLOAT,
                 weather_descriptions TEXT,
                 wind_speed FLOAT,
                 time TIMESTAMP,
                 inserted_at TIMESTAMP DEFAULT NOW(),
                 utc_offset TEXT
             ) ;         
         """)
        conn.commit()
        print("table was created.")
    except psycopg2.Error as e:
        print(f"Failed to create table: {e}")
        raise
    

def insert_records(conn, data):
    print("Inserting weather data into the database...")
    try:
        # Ensure the response is a dictionary
        if not isinstance(data, dict):
            raise ValueError(f"Unexpected data format: {type(data)}")

        # Check if API returned an error message
        if "error" in data:
            raise ValueError(f"Weather API returned error: {data['error']}")

        # Extract required keys from API response
        location = data.get("location")
        weather = data.get("current")

        # Ensure required keys exist
        if not location or not weather:
            raise KeyError(
                f"Missing required keys in API response. "
                f"Available keys: {list(data.keys())}"
            )

        cursor = conn.cursor()
        # Insert weather record into database table
        cursor.execute("""
            INSERT INTO dev.raw_weather_data(
                city,
                temperature,
                weather_descriptions,
                wind_speed,
                time,
                inserted_at,
                utc_offset
            ) VALUES (%s, %s, %s, %s, %s, NOW(), %s)
        """, (
            location.get("name"),
            weather.get("temperature"),
            (weather.get("weather_descriptions") or ["N/A"])[0],
            weather.get("wind_speed"),
            location.get("localtime") or datetime.utcnow(),
            location.get("utc_offset"),
        ))
        conn.commit()
        print("Data successfully inserted.")
    except (psycopg2.Error, KeyError, ValueError) as e:
        print(f"Error inserting data into the database: {e}")
        raise


def main():
    try:
        # Fetch data from API
        data = fetch_data()
        # Connect to database
        conn = connect_to_db()
        # Ensure table exists
        create_table(conn)
        # Insert weather data
        insert_records(conn, data)   
    except Exception as e:
        print(f"An error occured during execution: {e}")
    finally:
        # Close database connection safely
        if 'conn' in locals():
            conn.close() # type: ignore
            print("Database connection closed.")
    
main()   # Run main function
