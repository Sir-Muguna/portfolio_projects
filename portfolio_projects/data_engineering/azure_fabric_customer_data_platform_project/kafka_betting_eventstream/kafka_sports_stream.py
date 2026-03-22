import threading
import uuid
import random
import json
import time
import datetime
import logging
import pandas as pd  # Required to load user IDs from CSV
from faker import Faker
from confluent_kafka import Producer
from concurrent.futures import ThreadPoolExecutor

# === CONFIGURATION ===

TOPICS = {
    "betting_events": 2000,         # Heavy traffic
    "match_metadata": 200,          # Low volume
    "live_odds_updates": 400,       # Moderate
    "bet_results": 1500             # High
}

SEND_INTERVAL_SECONDS = 20
NUM_THREADS = len(TOPICS)
MATCH_POOL_SIZE = 1000
CORRUPT_PROBABILITY = 0.1
NULL_PROBABILITY = 0.01

fake = Faker()
match_pool = [f"MATCH_{i}" for i in range(1, MATCH_POOL_SIZE + 1)]

# === LOAD USER IDs FROM CSV ===
users_df = pd.read_csv("/root/projects/portfolio_projects/data_engineering/azure_fabric_customer_data_platform_project/data/users.csv")
user_ids = users_df['user_id'].dropna().astype(str).tolist()

# === LOGGER SETUP ===
logging.basicConfig(level=logging.INFO, format='[%(asctime)s][%(levelname)s] %(message)s')

# === UTILITY FUNCTIONS ===

def read_config():
    config = {}
    with open("client.properties") as fh:
        for line in fh:
            line = line.strip()
            if line and not line.startswith("#"):
                key, value = line.split("=", 1)
                config[key.strip()] = value.strip()
    return config


def corrupt_value(val, corrupt_chance=CORRUPT_PROBABILITY, null_chance=NULL_PROBABILITY):
    if random.random() < null_chance:
        return None
    if random.random() < corrupt_chance:
        if isinstance(val, str):
            return ''.join(random.sample(val, len(val)))
        elif isinstance(val, float):
            return val * random.choice([-1, 0])
    return val


def format_time(base_time):
    return base_time.strftime('%Y-%m-%dT%H:%M:%SZ')


# === EVENT GENERATORS ===

def generate_betting_events(count, base_time):
    return [{
        "event_id": str(uuid.uuid4()),
        "user_id": random.choice(user_ids),
        "match_id": random.choice(match_pool),
        "bet_type": corrupt_value(random.choice(["Full-time Win", "Draw", "Over/Under", "HT/FT"])),
        "stake_amount": corrupt_value(round(random.uniform(5, 5000), 2)),
        "odds": corrupt_value(round(random.uniform(1.2, 10.0), 2)),
        "bet_time": format_time(base_time),
        "device_id": str(uuid.uuid4()),
        "channel": corrupt_value(random.choice(["Web", "Mobile", "Retail"]))
    } for _ in range(count)]



# Define valid sport-league mappings
sport_league_map = {
    "Football": "Premier League",
    "Basketball": "NBA",
    "Cricket": "IPL",
    "Tennis": "ATP Tour",
    "Baseball": "MLB",
    "Hockey": "NHL",
    "Rugby": "Six Nations",
    "Formula 1": "FIA Formula One"
}

# Example match pool
match_pool = [f"match_{i}" for i in range(1, 101)]

def generate_match_metadata(count, base_time):
    events = []
    while len(events) < count:
        match_id = random.choice(match_pool)
        sport = random.choice(list(sport_league_map.keys()))
        league = sport_league_map[sport]

        event = {
            "match_id": match_id,
            "sport": corrupt_value(sport),
            "league": corrupt_value(league),
            "home_team": fake.city(),
            "away_team": fake.city(),
            "match_start_time": format_time(base_time + datetime.timedelta(minutes=random.randint(10, 120))),
            "status": corrupt_value(random.choice(["Scheduled", "Live", "Finished"]))
        }

        # Ensure no missing values
        if all(event[field] for field in ["sport", "league", "home_team", "away_team", "status"]):
            events.append(event)

    return events


def generate_live_odds_updates(count, base_time):
    events = []
    while len(events) < count:
        event = {
            "update_id": str(uuid.uuid4()),
            "match_id": random.choice(match_pool),
            "timestamp": format_time(base_time),
            "market": corrupt_value(random.choice(["1X2", "Over/Under", "Handicap", "First Half"])),
            "odds_home": corrupt_value(round(random.uniform(1.1, 5.0), 2)),
            "odds_draw": corrupt_value(round(random.uniform(1.0, 4.0), 2)),
            "odds_away": corrupt_value(round(random.uniform(1.5, 6.0), 2))
        }
        if (
            event["market"] and isinstance(event["odds_home"], (int, float)) and event["odds_home"] > 0 and
            isinstance(event["odds_draw"], (int, float)) and event["odds_draw"] > 0 and
            isinstance(event["odds_away"], (int, float)) and event["odds_away"] > 0
        ):
            events.append(event)
    return events


def generate_bet_results(count, base_time):
    return [{
        "event_id": str(uuid.uuid4()),
        "match_id": random.choice(match_pool),
        "user_id": random.choice(user_ids),
        "outcome": corrupt_value(random.choice(["Win", "Loss", "Cancelled", "Void"])),
        "settlement_amount": corrupt_value(round(random.uniform(0, 10000), 2)),
        "settlement_time": format_time(base_time + datetime.timedelta(minutes=random.randint(1, 60)))
    } for _ in range(count)]


# Mapping topic to generator
TOPIC_GENERATORS = {
    "betting_events": generate_betting_events,
    "match_metadata": generate_match_metadata,
    "live_odds_updates": generate_live_odds_updates,
    "bet_results": generate_bet_results
}


# === PRODUCER ===

def send_topic_events(producer, topic, count, base_time):
    events = TOPIC_GENERATORS[topic](count, base_time)
    for event in events:
        key = event.get("match_id", str(uuid.uuid4()))
        producer.produce(topic, key=key.encode(), value=json.dumps(event).encode())
    logging.info(f"[Producer] Sent {len(events):,} records to topic: {topic}")


def producer_main(config, duration_minutes=10):
    producer = Producer(config)
    logging.info(f"[Producer] Starting for {duration_minutes} minutes")

    start = time.time()
    try:
        while (time.time() - start) < duration_minutes * 60:
            base_time = datetime.datetime.utcnow()
            with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
                for topic, count in TOPICS.items():
                    executor.submit(send_topic_events, producer, topic, count, base_time)

            producer.flush()
            logging.info("[Producer] Batch complete. Sleeping 20 seconds.")
            time.sleep(SEND_INTERVAL_SECONDS)
    except KeyboardInterrupt:
        logging.warning("[Producer] Interrupted by user")
    finally:
        producer.flush()
        logging.info("[Producer] Shutdown complete")


# === MAIN ===

if __name__ == "__main__":
    config = read_config()
    producer_main(config, duration_minutes=60)  # Run for 60 minutes
