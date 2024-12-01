import pymongo
from faker import Faker
from datetime import datetime, timedelta
import random

# Initialize MongoDB client and database
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["robot_simulator"]

# Initialize Faker
faker = Faker()

# Collections
sensors_collection = db["sensors"]
alert_logs_collection = db["alert_logs"]
images_collection = db["images"]
simulation_data_collection = db["simulation_data"]

# Function to create sample sensor data
def create_sample_sensors(num_records=10):
    for _ in range(num_records):
        sensor_data = {
            "robot_id": random.randint(1, 5),
            "sensor_type": random.choice(["temperature", "motion", "camera"]),
            "readings": {"value": round(random.uniform(15.0, 35.0), 2), "unit": "C"},
            "timestamp": faker.date_time_this_year()
        }
        sensors_collection.insert_one(sensor_data)
    print(f"Inserted {num_records} sample sensor records.")

# Function to create sample alert logs
def create_sample_alert_logs(num_records=10):
    for _ in range(num_records):
        alert_log = {
            "robot_id": random.randint(1, 5),
            "alert_type": random.choice(["low_battery", "intruder_detected", "obstacle"]),
            "severity": random.choice(["low", "medium", "high"]),
            "timestamp": faker.date_time_this_year(),
            "metadata": {"details": faker.sentence()}
        }
        alert_logs_collection.insert_one(alert_log)
    print(f"Inserted {num_records} sample alert log records.")

# Function to create sample image data
def create_sample_images(num_records=5):
    for _ in range(num_records):
        image_data = {
            "robot_id": random.randint(1, 5),
            "sensor_id": faker.uuid4(),
            "images": [faker.image_url() for _ in range(3)],
            "timestamp": faker.date_time_this_year()
        }
        images_collection.insert_one(image_data)
    print(f"Inserted {num_records} sample image records.")

# Function to create sample simulation data
def create_sample_simulation_data(num_records=5):
    for _ in range(num_records):
        simulation_data = {
            "robot_id": random.randint(1, 5),
            "simulation_config": {
                "speed": random.randint(1, 10),
                "patrol_area": faker.address()
            },
            "start_time": faker.date_time_this_year(),
            "end_time": faker.date_time_this_year(),
            "result": random.choice(["success", "failure"])
        }
        simulation_data_collection.insert_one(simulation_data)
    print(f"Inserted {num_records} sample simulation data records.")

# Populate all collections with sample data
create_sample_sensors()
create_sample_alert_logs()
create_sample_images()
create_sample_simulation_data()

print("Sample data creation completed.")
