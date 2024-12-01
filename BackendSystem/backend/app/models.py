from .database import mysql
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from .optimization import optimize_patrol_path
from datetime import timedelta

# Initialize MongoDB client and database
mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["robot_simulator"]

def execute_crud_operation(table_name, operation, data=None, record_id=None, use_mongodb=False):
    if use_mongodb:
        # Handle MongoDB CRUD operations
        collection = mongo_db[table_name]
        print("collection", collection)
        try:
            if operation == "create":
                if not data:
                    return {"error": "Data is required to create a record"}, 400
                data["timestamp"] = datetime.now()
                result = collection.insert_one(data)
                return {"message": "Document created successfully!", "id": str(result.inserted_id)}, 201

            elif operation == "read":
                print("read")
                if data and "robot_id" in data:
                    print("data", data)
                    # Filter based on `robot_id` if provided in the data
                    documents = list(collection.find({"robot_id": int(data["robot_id"])}))
                else:
                    # Fetch all documents if no `robot_id` is provided
                    documents = list(collection.find())
                # Convert ObjectId to string for each document
                for doc in documents:
                    doc["_id"] = str(doc["_id"])
                return documents, 200
            
            elif operation == "update":
                if not record_id or not data:
                    return {"error": "Record ID and data are required for update"}, 400
                result = collection.update_one(
                    {"_id": ObjectId(record_id)}, {"$set": data}
                )
                if result.matched_count == 0:
                    return {"message": f"No document found with ID {record_id}"}, 404
                return {"message": "Document updated successfully!"}, 200

            elif operation == "delete":
                if not record_id:
                    return {"error": "Record ID is required for delete"}, 400
                result = collection.delete_one({"_id": ObjectId(record_id)})
                if result.deleted_count == 0:
                    return {"message": f"No document found with ID {record_id}"}, 404
                return {"message": "Document deleted successfully!"}, 200

            else:
                return {"error": "Invalid operation"}, 400

        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}, 500

    else:
        # Handle MySQL CRUD operations
        cursor = None
        try:
            cursor = mysql.connection.cursor()
            if operation == "create":
                if not data:
                    return {"error": "Data is required to create a record"}, 400
                columns = ", ".join(data.keys())
                values_placeholders = ", ".join(["%s"] * len(data))
                sql = f"INSERT INTO `{table_name}` ({columns}) VALUES ({values_placeholders})"
                cursor.execute(sql, tuple(data.values()))
                mysql.connection.commit()
                return {"message": f"Record created successfully in {table_name}"}, 201

            elif operation == "read":
                try:
                    print("read","data",data)
                    if data and "robot_id" in data.keys():
                        print("data", data)
                        # If `robot_id` is provided in the data, filter based on `robot_id`
                        robot_id = data["robot_id"]
                        sql = f"SELECT * FROM `{table_name}` WHERE robot_id = %s"
                        cursor.execute(sql, (robot_id,))
                    else:
                        # Otherwise, fetch all records
                        sql = f"SELECT * FROM `{table_name}`"
                        cursor.execute(sql)
                    
                    records = cursor.fetchall()
                    if not records:
                        return {"message": f"No records found in {table_name}"}, 404
                    
                    # Format the records into a list of dictionaries
                    columns = [desc[0] for desc in cursor.description]
                    formatted_records = [dict(zip(columns, record)) for record in records]
                    return formatted_records, 200

                except Exception as e:
                    return {"error": f"An error occurred: {str(e)}"}, 500


            elif operation == "update":
                if not record_id or not data:
                    return {"error": "Record ID and data are required for update"}, 400
                set_clause = ", ".join([f"{key}=%s" for key in data.keys()])
                sql = f"UPDATE `{table_name}` SET {set_clause} WHERE id=%s"
                print("sql",sql,tuple(data.values()) + (record_id,))
                cursor.execute(sql, tuple(data.values()) + (record_id,))
                mysql.connection.commit()
                print("cursor.rowcount",cursor.rowcount)
                if cursor.rowcount == 0:
                    return {"message": f"No record found with ID {record_id} in {table_name}"}, 404
                return {"message": f"Record updated successfully in {table_name}"}, 200

            elif operation == "delete":
                if not record_id:
                    return {"error": "Record ID is required for delete"}, 400
                sql = f"DELETE FROM `{table_name}` WHERE id=%s"
                cursor.execute(sql, (record_id,))
                mysql.connection.commit()
                if cursor.rowcount == 0:
                    return {"message": f"No record found with ID {record_id} in {table_name}"}, 404
                return {"message": f"Record deleted successfully from {table_name}"}, 200

            else:
                return {"error": "Invalid operation"}, 400

        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}, 500

        finally:
            if cursor:
                cursor.close()

# Function to get the list of MySQL tables
def get_table_names():
    try:
        connection = mysql.connection
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        cursor.close()
        return tables
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

# Function to get the list of MongoDB collections
def get_collection_names():
    try:
        collections = mongo_db.list_collection_names()
        return collections
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

from .database import mysql

def get_total_robots():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM robots")
    total_robots = cursor.fetchone()[0]
    cursor.close()
    return total_robots

def get_active_robots():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM robot_status WHERE status = 'Active'")
    active_robots = cursor.fetchone()[0]
    cursor.close()
    return active_robots

def get_alerts():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, alert_type AS type, description AS message, alert_time AS timestamp FROM service_alerts ORDER BY alert_time DESC LIMIT 5")
    alerts = cursor.fetchall()
    cursor.close()
    return [
        {
            "id": alert[0],
            "type": alert[1],
            "message": alert[2],
            "timestamp": alert[3].strftime("%Y-%m-%d %H:%M:%S")
        }
        for alert in alerts
    ]

def get_average_speed():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT AVG(battery_level) FROM robot_status")
    average_speed = cursor.fetchone()[0] or 0
    cursor.close()
    return average_speed

def get_completion_time():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT AVG(TIMESTAMPDIFF(MINUTE, start_time, end_time)) FROM patrol_schedules")
    completion_time = cursor.fetchone()[0] or 0
    cursor.close()
    return completion_time

def get_stop_count():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM robot_status WHERE status = 'Stopped'")
    stop_count = cursor.fetchone()[0]
    cursor.close()
    return stop_count

from .database import mysql
from datetime import datetime

# Function to create a new patrol schedule
def create_patrol_schedule(data):
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        sql = """
            INSERT INTO patrol_schedules (robot_id, staff_id, start_time, end_time, path_details, created_at)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        # robot_id is compulsory, others have default values
        robot_id = data["robot_id"]
        staff_id = data.get("staff_id", 1)
        start_time = data.get("start_time", "2024-01-01 08:00:00")
        end_time = data.get("end_time", "2024-01-01 10:00:00")
        path_details = data.get("path_details", "Default patrol route")
        
        cursor.execute(
            sql,
            (robot_id, staff_id, start_time, end_time, path_details, datetime.now())
        )
        mysql.connection.commit()
        schedule_id = cursor.lastrowid
        return {"message": "Patrol schedule created successfully", "schedule_id": schedule_id}, 201
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}, 500
    finally:
        if cursor:
            cursor.close()

# Function to optimize an existing patrol schedule
def optimize_patrol_schedule(schedule_id, data):
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        # Example optimization logic based on criteria
        criteria = data.get("criteria", "default_criteria")
        optimized_path_details = "[]"  # Placeholder for optimized path logic
        # Update the patrol schedule with optimized path details
        sql = "UPDATE patrol_schedules SET path_details = %s WHERE id = %s"
        cursor.execute(sql, (optimized_path_details, schedule_id))
        mysql.connection.commit()
        return {"message": "Patrol schedule optimized successfully", "optimizedPathDetails": optimized_path_details}, 200
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}, 500
    finally:
        if cursor:
            cursor.close()

# Function to get all patrol schedules for a specific robot
def get_schedules_for_robot(robot_id):
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        sql = """
            SELECT id, staff_id, start_time, end_time, path_details 
            FROM patrol_schedules 
            WHERE robot_id = %s
        """
        cursor.execute(sql, (robot_id,))
        records = cursor.fetchall()
        if not records:
            return [], 200
        schedules = [
            {
                "schedule_id": record[0],
                "staff_id": record[1],
                "start_time": record[2].strftime("%Y-%m-%d %H:%M:%S"),
                "end_time": record[3].strftime("%Y-%m-%d %H:%M:%S"),
                "path_details": record[4]
            }
            for record in records
        ]
        return {"robot_id": robot_id, "schedules": schedules}, 200
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}, 500
    finally:
        if cursor:
            cursor.close()

# Function to delete a patrol schedule
def delete_patrol_schedule(schedule_id):
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        sql = "DELETE FROM patrol_schedules WHERE id = %s"
        cursor.execute(sql, (schedule_id,))
        mysql.connection.commit()
        if cursor.rowcount == 0:
            return {"message": f"No patrol schedule found with ID {schedule_id}"}, 404
        return {"message": "Patrol schedule deleted successfully"}, 200
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}, 500
    finally:
        if cursor:
            cursor.close()

############################################
# Path API endpoints                       #
############################################
patrol_paths_collection = mongo_db["patrol_paths"]

def create_patrol_path(data):
    try:
        # Validate required fields
        if "robot_id" not in data or "waypoints" not in data or "staff_id" not in data:
            return {"error": "robot_id, waypoints, and staff_id are required fields"}, 400

        # Verify robot exists and is active
        robot_status = execute_crud_operation("robot_status", "read", data={"robot_id": data["robot_id"]})
        if robot_status[1] != 200:
            return {"error": f"Robot with ID {data['robot_id']} not found or inactive"}, 404
        
        # Check robot's battery level
        battery_level = robot_status[0][0].get("battery_level", 0)
        if battery_level < 20:
            return {"error": f"Robot battery level too low ({battery_level}%). Minimum 20% required."}, 400

        # Verify staff exists and has appropriate role
        staff_query = f"SELECT role FROM system_staff WHERE id = {data['staff_id']}"
        cursor = mysql.connection.cursor()
        cursor.execute(staff_query)
        staff_result = cursor.fetchone()
        cursor.close()

        if not staff_result:
            return {"error": f"Staff member with ID {data['staff_id']} not found"}, 404

        staff_role = staff_result[0]
        allowed_roles = ["Security Engineer", "Manager", "Operator"]
        if staff_role not in allowed_roles:
            return {"error": f"Staff role '{staff_role}' not authorized to create patrol paths"}, 403

        # Process waypoints
        processed_waypoints = []
        for point in data["waypoints"]:
            processed_waypoints.append({
                "latitude": float(point["latitude"]),
                "longitude": float(point["longitude"]),
                "timestamp": None  # Will be calculated during optimization
            })

        # Add metadata and timestamps
        path_data = {
            "robot_id": data["robot_id"],
            "staff_id": data["staff_id"],
            "waypoints": processed_waypoints,
            "created_at": datetime.now(),
            "status": "pending",
            "metadata": {
                "battery_level_at_creation": battery_level,
                "robot_location_at_creation": robot_status[0][0].get("location", "Unknown"),
                "total_waypoints": len(processed_waypoints),
                "estimated_completion_time": None,  # Will be calculated by optimization
                "total_distance": None,  # Will be calculated by optimization
                "estimated_battery_usage": None  # Will be calculated by optimization
            }
        }

        # Add schedule information
        path_data["schedule"] = {
            "start_time": data["schedule"]["start_time"].isoformat() if isinstance(data["schedule"]["start_time"], datetime) else data["schedule"]["start_time"],
            "end_time": data["schedule"]["end_time"].isoformat() if isinstance(data["schedule"]["end_time"], datetime) else data["schedule"]["end_time"],
            "repeat": data["schedule"].get("repeat", False),
            "frequency": data["schedule"].get("frequency", "once"),
            "created_at": datetime.now().isoformat()
        }

        # Insert into MongoDB
        result = patrol_paths_collection.insert_one(path_data)
        
        # Create a corresponding patrol schedule in MySQL
        schedule_data = {
            "robot_id": data["robot_id"],
            "staff_id": data["staff_id"],
            "start_time": data["schedule"]["start_time"],
            "end_time": data["schedule"]["end_time"],
            "path_details": f"Patrol path {result.inserted_id}",
            "status": "scheduled"
        }
        
        schedule_response = create_patrol_schedule(schedule_data)
        if schedule_response[1] != 201:
            # Rollback MongoDB insert if MySQL insert fails
            patrol_paths_collection.delete_one({"_id": result.inserted_id})
            return {"error": "Failed to create patrol schedule"}, 500

        return {
            "message": "Patrol path created successfully",
            "pathId": str(result.inserted_id),
            "scheduleId": schedule_response[0].get("schedule_id"),
            "metadata": path_data["metadata"],
            "schedule": path_data["schedule"]
        }, 201
        
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}, 500

# Function to retrieve all patrol paths for a specific robot
def get_paths_for_robot(robot_id):
    try:
        paths = list(patrol_paths_collection.find({"robot_id": robot_id}))
        for path in paths:
            path["_id"] = str(path["_id"])  # Convert ObjectId to string
        return paths, 200
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}, 500

def optimize_patrol_path(path_id, optimization_data):
    """
    Optimize a patrol path based on given criteria and constraints
    Args:
        path_id: MongoDB ObjectId of the path to optimize
        optimization_data: Dictionary containing optimization parameters
            {
                "criteria": ["battery", "coverage", "time", "obstacles"],
                "area_bounds": {
                    "min_x": float,
                    "max_x": float,
                    "min_y": float,
                    "max_y": float
                },
                "speed_limit": float,
                "obstacles": [{"x": float, "y": float}]
            }
    """
    try:
        # Retrieve the existing path
        path = patrol_paths_collection.find_one({"_id": ObjectId(path_id)})
        if not path:
            return {"error": f"Path with ID {path_id} not found"}, 404

        # Extract current waypoints and optimization parameters
        current_waypoints = path.get("waypoints", [])
        criteria = optimization_data.get("criteria", ["battery", "coverage", "time", "obstacles"])
        area_bounds = optimization_data.get("area_bounds")
        speed_limit = optimization_data.get("speed_limit")
        obstacles = optimization_data.get("obstacles", [])

        # Initialize optimization metrics
        optimization_stats = {
            "original_distance": 0,
            "optimized_distance": 0,
            "battery_saved": 0,
            "time_saved": 0,
            "coverage_improved": 0
        }

        # Apply optimization strategies based on criteria
        optimized_waypoints = current_waypoints.copy()
        
        if "battery" in criteria:
            # Optimize for battery efficiency
            optimized_waypoints = optimize_for_battery(optimized_waypoints, speed_limit)
            optimization_stats["battery_saved"] = calculate_battery_savings(current_waypoints, optimized_waypoints)

        if "coverage" in criteria:
            # Optimize for area coverage
            optimized_waypoints = optimize_for_coverage(optimized_waypoints, area_bounds)
            optimization_stats["coverage_improved"] = calculate_coverage_improvement(current_waypoints, optimized_waypoints, area_bounds)

        if "time" in criteria:
            # Optimize for time efficiency
            optimized_waypoints = optimize_for_time(optimized_waypoints, speed_limit)
            optimization_stats["time_saved"] = calculate_time_savings(current_waypoints, optimized_waypoints, speed_limit)

        if "obstacles" in criteria:
            # Apply obstacle avoidance
            optimized_waypoints = avoid_obstacles(optimized_waypoints, obstacles)

        # Calculate final distances
        optimization_stats["original_distance"] = calculate_total_distance(current_waypoints)
        optimization_stats["optimized_distance"] = calculate_total_distance(optimized_waypoints)

        # Update the path with optimized waypoints
        update_result = patrol_paths_collection.update_one(
            {"_id": ObjectId(path_id)},
            {
                "$set": {
                    "waypoints": optimized_waypoints,
                    "optimization_history": {
                        "timestamp": datetime.now(),
                        "criteria": criteria,
                        "stats": optimization_stats
                    },
                    "last_optimized": datetime.now()
                }
            }
        )

        if update_result.modified_count == 0:
            return {"error": "Failed to update path with optimized waypoints"}, 500

        return {
            "optimization_result": {
                "optimized_waypoints": optimized_waypoints,
                "total_waypoints": len(optimized_waypoints)
            },
            "optimization_stats": optimization_stats
        }, 200

    except Exception as e:
        return {"error": f"Error during path optimization: {str(e)}"}, 500

def optimize_for_battery(waypoints, speed_limit):
    # Implement battery optimization logic
    # This is a placeholder implementation
    return waypoints

def optimize_for_coverage(waypoints, area_bounds):
    # Implement coverage optimization logic
    # This is a placeholder implementation
    return waypoints

def optimize_for_time(waypoints, speed_limit):
    # Implement time optimization logic
    # This is a placeholder implementation
    return waypoints

def avoid_obstacles(waypoints, obstacles):
    # Implement obstacle avoidance logic
    # This is a placeholder implementation
    return waypoints

def calculate_total_distance(waypoints):
    # Calculate total distance between waypoints
    total_distance = 0
    for i in range(len(waypoints) - 1):
        lat1, lon1 = waypoints[i]["latitude"], waypoints[i]["longitude"]
        lat2, lon2 = waypoints[i + 1]["latitude"], waypoints[i + 1]["longitude"]
        total_distance += calculate_distance(lat1, lon1, lat2, lon2)
    return total_distance

def calculate_battery_savings(original_waypoints, optimized_waypoints):
    # Calculate estimated battery savings
    # This is a placeholder implementation
    return 0

def calculate_coverage_improvement(original_waypoints, optimized_waypoints, area_bounds):
    # Calculate coverage improvement percentage
    # This is a placeholder implementation
    return 0

def calculate_time_savings(original_waypoints, optimized_waypoints, speed_limit):
    # Calculate time savings in seconds
    # This is a placeholder implementation
    return 0

def calculate_distance(lat1, lon1, lat2, lon2):
    # Implement Haversine formula for calculating distance between coordinates
    # This is a placeholder implementation
    return 0

# Function to delete a patrol path
def delete_patrol_path(path_id):
    try:
        result = patrol_paths_collection.delete_one({"_id": ObjectId(path_id)})
        if result.deleted_count == 0:
            return {"message": f"No path found with ID {path_id}"}, 404
        return {"message": "Patrol path deleted successfully"}, 200
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}, 500