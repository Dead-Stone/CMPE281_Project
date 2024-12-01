import carla

try:
    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)
    print("Successfully connected to CARLA!")
except Exception as e:
    print("Error connecting to CARLA:", e)



import requests
import time

# Constants for CARLA and Backend API
CARLA_HOST = 'localhost'
CARLA_PORT = 2000
BACKEND_API_BASE_URL = 'http://localhost:5000/api'

# Function to connect to the CARLA simulator
def connect_to_carla():
    client = carla.Client(CARLA_HOST, CARLA_PORT)
    client.set_timeout(10.0)
    return client.get_world()

# Function to gather vehicle data from the CARLA world
def gather_vehicle_data(world):
    vehicles = world.get_actors().filter('vehicle.*')
    vehicle_data = []

    for vehicle in vehicles:
        transform = vehicle.get_transform()
        velocity = vehicle.get_velocity()
        battery_level = 100  # Placeholder value; replace with actual sensor data if available

        vehicle_data.append({
            'id': vehicle.id,
            'location': f"{transform.location.x}, {transform.location.y}, {transform.location.z}",
            'speed': (velocity.x**2 + velocity.y**2 + velocity.z**2) ** 0.5,
            'battery_level': battery_level,
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
        })

    return vehicle_data

# Function to send data to the backend API
def send_data_to_backend(data):
    try:
        response = requests.post(f"{BACKEND_API_BASE_URL}/robot_status/create", json=data)
        if response.status_code == 201:
            print("Data sent successfully:", data)
        else:
            print("Failed to send data:", response.json())
    except Exception as e:
        print("Error while sending data to backend:", str(e))

# Main loop to continuously gather and send data
def main():
    world = connect_to_carla()
    print("Connected to CARLA simulator")

    while True:
        vehicle_data = gather_vehicle_data(world)
        for data in vehicle_data:
            send_data_to_backend(data)

        time.sleep(1)  # Adjust the interval as needed

if __name__ == "__main__":
    main()
