from datetime import datetime
from flask import request, jsonify
from . import app
from .models import create_patrol_path, delete_patrol_path, execute_crud_operation, get_collection_names, get_table_names, get_total_robots, get_active_robots, get_alerts, get_average_speed, get_completion_time, get_stop_count, create_patrol_schedule, optimize_patrol_schedule, get_schedules_for_robot, delete_patrol_schedule, optimize_patrol_path, get_paths_for_robot    
from bson import ObjectId

# Common CRUD Endpoints
@app.route('/api/<table_name>/create', methods=['POST'])
def create_record(table_name):
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    response, status_code = execute_crud_operation(table_name, "create", data=data)
    return jsonify(response), status_code

@app.route('/api/<table_name>/read', methods=['GET'])
def read_records(table_name):
    # Check for the 'useMongo' flag in the query parameters
    use_mongo = request.args.get('use_mongodb', 'false').lower() == 'true'
    # Call the execute_crud_operation function with the 'use_mongodb' flag
    response, status_code = execute_crud_operation(table_name, "read", use_mongodb=use_mongo)
    # Check if the response contains no data
    if status_code == 200 and not response:
        return jsonify({"message": "No data available in the table"}), 404
    return jsonify(response), status_code


@app.route('/api/<table_name>/update/<record_id>', methods=['PUT'])
def update_record(table_name, record_id):
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    response, status_code = execute_crud_operation(table_name, "update", data=data, record_id=record_id)
    return jsonify(response), status_code

@app.route('/api/<table_name>/delete/<record_id>', methods=['DELETE'])
def delete_record(table_name, record_id):
    response, status_code = execute_crud_operation(table_name, "delete", record_id=record_id)
    return jsonify(response), status_code

# API to get a list of tables (for MySQL) or collections (for MongoDB)
@app.route('/api/list_tables', methods=['GET'])
def list_tables():
    db_type = request.args.get('db_type', 'mysql').lower()

    if db_type == 'mysql':
        tables = get_table_names()
        return jsonify({"tables": tables}), 200
    elif db_type == 'mongodb':
        collections = get_collection_names()
        return jsonify({"collections": collections}), 200
    else:
        return jsonify({"error": "Invalid database type. Use 'mysql' or 'mongodb'."}), 400
    
# Security Service Alert Management Endpoints

# Endpoint to create a new alert
@app.route('/api/alerts/create', methods=['POST'])
def create_alert():
    data = request.json
    print("create_alert_data::::::::::::::::::::::::::::::::", data)
    if not data:
        return jsonify({"error": "No data provided"}), 400
    response, status_code = execute_crud_operation("service_alerts", "create", data=data)
    return jsonify(response), status_code

# Endpoint to fetch all alerts
@app.route('/api/alerts', methods=['GET'])
def get_all_alerts():
    response, status_code = execute_crud_operation("service_alerts", "read")
    if status_code == 200 and not response:
        return jsonify({"message": "No alerts found"}), 404
    return jsonify(response), status_code

# Endpoint to fetch alerts by Robot ID
@app.route('/api/alerts/<int:robot_id>', methods=['GET'])
def get_alerts_by_robot_id(robot_id):
    filters = {"robot_id": robot_id}
    print("filters", filters)
    response, status_code = execute_crud_operation("service_alerts", "read", data=filters)
    if status_code == 200 and not response:
        return jsonify({"message": f"No alerts found for Robot ID {robot_id}"}), 404
    return jsonify({"alerts": response}), status_code


# Endpoint to delete an alert
@app.route('/api/alerts/delete/<record_id>', methods=['DELETE'])
def delete_alert(record_id):
    response, status_code = execute_crud_operation("service_alerts", "delete", record_id=record_id)
    return jsonify(response), status_code


# Endpoint to update robot status based on the alert information
@app.route('/api/alerts/update_robot_status/<alert_id>', methods=['PUT'])
def update_robot_status(alert_id):
    data = request.json
    print("update_robot_status_data", data)

    # Validate that the required fields are provided
    if not data or "status" not in data:
        return jsonify({"error": "Status is required to update the robot status"}), 400

    # Extract the robot_id from the alert information
    alert_response, alert_status_code = execute_crud_operation("service_alerts", "read", record_id=alert_id)
    
    if alert_status_code != 200 or not alert_response:
        return jsonify({"error": f"No alert found with ID {alert_id}"}), 404

    # Assuming alert_response is a list of one dictionary, extract the robot_id
    alert = alert_response[0]
    robot_id = alert.get("robot_id")

    if not robot_id:
        return jsonify({"error": "Robot ID is missing in the alert information"}), 400

    # Prepare data to update the robot_status table
    robot_status_data = {"status": data["status"]}

    # Update the robot_status table using the execute_crud_operation function
    response, status_code = execute_crud_operation("robot_status", "update", data=robot_status_data, record_id=robot_id)

    if status_code == 200:
        return jsonify({"message": "Robot status updated successfully!"}), 200
    else:
        return jsonify(response), status_code

from .models import get_total_robots, get_active_robots, get_alerts, get_average_speed, get_completion_time, get_stop_count

# =========================
# System Dashboard Endpoints
# =========================

@app.route('/api/dashboard/overview', methods=['GET'])
def get_dashboard_overview():
    try:
        total_robots = get_total_robots()
        active_robots = get_active_robots()
        alerts = get_alerts()
        average_speed = get_average_speed()
        completion_time = get_completion_time()

        overview_data = {
            "totalRobots": total_robots,
            "activeRobots": active_robots,
            "alerts": alerts,
            "averageSpeed": average_speed,
            "completionTime": completion_time
        }
        return jsonify(overview_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/dashboard/metrics/completion-time', methods=['GET'])
def get_completion_time_metrics():
    try:
        completion_time = get_completion_time()
        return jsonify({"averageCompletionTime": completion_time}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/dashboard/metrics/average-speed', methods=['GET'])
def get_average_speed_metrics():
    try:
        average_speed = get_average_speed()
        return jsonify({"averageSpeed": average_speed}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/dashboard/metrics/stop-count', methods=['GET'])
def get_stop_count_metrics():
    try:
        stop_count = get_stop_count()
        return jsonify({"stopCount": stop_count}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/dashboard/metrics/alerts', methods=['GET'])
def get_alert_metrics():
    try:
        alerts = get_alerts()
        return jsonify(alerts), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


from flask import request, jsonify
from . import app
from .models import (
    create_patrol_schedule,
    optimize_patrol_schedule,
    get_schedules_for_robot,
    delete_patrol_schedule
)

# =========================
# Patrol Schedule Endpoints
# =========================

# Endpoint to create a new patrol schedule
@app.route('/api/patrol_schedules', methods=['POST'])
def create_patrol_schedule_endpoint():
    data = request.json

    # Check if `robot_id` is provided
    if "robot_id" not in data or not data["robot_id"]:
        return jsonify({"error": "robot_id is required"}), 400

    # Hardcode default values for other fields if not supplied
    staff_id = data.get("staff_id", 1)  # Default staff_id = 1
    start_time = data.get("start_time", "2024-01-01 08:00:00")  # Default start_time
    end_time = data.get("end_time", "2024-01-01 10:00:00")  # Default end_time
    path_details = data.get("path_details", "Default patrol route")  # Default path_details

    # Create a dictionary to pass to the model
    schedule_data = {
        "robot_id": data["robot_id"],
        "staff_id": staff_id,
        "start_time": start_time,
        "end_time": end_time,
        "path_details": path_details
    }
    
    response, status_code = create_patrol_schedule(schedule_data)
    return jsonify(response), status_code

# Endpoint to optimize an existing patrol schedule
@app.route('/api/patrol_schedules/<int:schedule_id>/optimize', methods=['PUT'])
def optimize_patrol_schedule_endpoint(schedule_id):
    data = request.json

    # Hardcode default optimization criteria if not supplied
    criteria = data.get("criteria", "default_criteria")

    response, status_code = optimize_patrol_schedule(schedule_id, {"criteria": criteria})
    return jsonify(response), status_code

# Endpoint to retrieve all patrol schedules for a specific robot
@app.route('/api/patrol_schedules/<int:robot_id>', methods=['GET'])
def get_robot_schedules(robot_id):
    response, status_code = get_schedules_for_robot(robot_id)
    if status_code == 200 and not response:
        return jsonify({"message": f"No patrol schedules found for Robot ID {robot_id}"}), 404
    return jsonify(response), status_code

# Endpoint to delete a patrol schedule
@app.route('/api/patrol_schedules/<int:schedule_id>', methods=['DELETE'])
def delete_patrol_schedule_endpoint(schedule_id):
    response, status_code = delete_patrol_schedule(schedule_id)
    return jsonify(response), status_code


# =========================
# Path Configuration Endpoints
# =========================

# Endpoint to create a new patrol path
@app.route("/api/patrol/path", methods=["POST"])
def create_patrol_path_endpoint():
    try:
        data = request.get_json()
        
        # Basic request validation
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        required_fields = ["robot_id", "staff_id", "waypoints"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
                
        # Validate waypoints format
        if not isinstance(data["waypoints"], list) or not data["waypoints"]:
            return jsonify({"error": "Waypoints must be a non-empty list"}), 400
            
        for point in data["waypoints"]:
            if not isinstance(point, dict) or "latitude" not in point or "longitude" not in point:
                return jsonify({"error": "Each waypoint must contain latitude and longitude coordinates"}), 400
            
            # Validate coordinate ranges
            if not (-90 <= float(point["latitude"]) <= 90):
                return jsonify({"error": "Latitude must be between -90 and 90 degrees"}), 400
            if not (-180 <= float(point["longitude"]) <= 180):
                return jsonify({"error": "Longitude must be between -180 and 180 degrees"}), 400
                
        # Create schedule data
        schedule_data = {
            "start_time": data.get("start_time", datetime.now().isoformat()),
            "end_time": data.get("end_time"),
            "repeat": data.get("repeat", False),
            "frequency": data.get("frequency", "once")
        }
        
        # Validate schedule times
        try:
            if schedule_data["start_time"]:
                schedule_data["start_time"] = datetime.fromisoformat(schedule_data["start_time"].replace('Z', '+00:00'))
            if schedule_data["end_time"]:
                schedule_data["end_time"] = datetime.fromisoformat(schedule_data["end_time"].replace('Z', '+00:00'))
                if schedule_data["end_time"] <= schedule_data["start_time"]:
                    return jsonify({"error": "End time must be after start time"}), 400
        except ValueError as e:
            return jsonify({"error": f"Invalid datetime format. Use ISO format (YYYY-MM-DDTHH:MM:SS): {str(e)}"}), 400
        
        # Add schedule to the main data
        data["schedule"] = schedule_data
        
        # Create the patrol path
        result, status_code = create_patrol_path(data)
        
        if status_code != 201:
            return jsonify(result), status_code
            
        # Log successful path creation
        app.logger.info(f"Created patrol path for robot {data['robot_id']} by staff {data['staff_id']}")
        
        return jsonify(result), status_code
        
    except Exception as e:
        app.logger.error(f"Error creating patrol path: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

# Endpoint to optimize an existing patrol path
@app.route('/api/paths/<path_id>/optimize', methods=['PUT'])
def optimize_patrol_path_endpoint(path_id):
    """
    Optimize a patrol path based on various criteria
    Expected payload:
    {
        "criteria": ["battery", "coverage", "time", "obstacles"],
        "area_bounds": {
            "min_x": float,
            "max_x": float,
            "min_y": float,
            "max_y": float
        },
        "speed_limit": float,
        "obstacles": [
            {"x": float, "y": float}
        ]
    }
    """
    try:
        data = request.json or {}
        print(f"Received optimization request for path {path_id} with data: {data}")
        
        # Validate path_id format for MongoDB ObjectId
        try:
            path_object_id = ObjectId(path_id)
            print(f"Valid path ID: {path_id}")
        except:
            return jsonify({"error": "Invalid path ID format"}), 400

        # Validate area bounds if provided
        if "area_bounds" in data:
            bounds = data["area_bounds"]
            required_bounds = ["min_x", "max_x", "min_y", "max_y"]
            if not all(key in bounds for key in required_bounds):
                return jsonify({"error": "area_bounds must include min_x, max_x, min_y, and max_y"}), 400
            if not all(isinstance(bounds[key], (int, float)) for key in required_bounds):
                return jsonify({"error": "all bound values must be numbers"}), 400
            # Validate bound ranges
            if bounds["min_x"] >= bounds["max_x"] or bounds["min_y"] >= bounds["max_y"]:
                return jsonify({"error": "Invalid bound ranges: min values must be less than max values"}), 400
        print(f"Valid area bounds: {data.get('area_bounds')}")

        # Validate speed limit if provided
        if "speed_limit" in data:
            if not isinstance(data["speed_limit"], (int, float)):
                return jsonify({"error": "speed_limit must be a number"}), 400
            if data["speed_limit"] <= 0:
                return jsonify({"error": "speed_limit must be greater than 0"}), 400
        print(f"Valid speed limit: {data.get('speed_limit')}")

        # Validate obstacles if provided
        if "obstacles" in data:
            if not isinstance(data["obstacles"], list):
                return jsonify({"error": "obstacles must be a list of points"}), 400
            for obstacle in data["obstacles"]:
                if not isinstance(obstacle, dict) or "x" not in obstacle or "y" not in obstacle:
                    return jsonify({"error": "each obstacle must have x and y coordinates"}), 400
                if not isinstance(obstacle["x"], (int, float)) or not isinstance(obstacle["y"], (int, float)):
                    return jsonify({"error": "obstacle coordinates must be numbers"}), 400
        print(f"Valid obstacles: {data.get('obstacles')}")

        # Validate optimization criteria
        valid_criteria = ["battery", "coverage", "time", "obstacles"]
        if "criteria" in data:
            if not isinstance(data["criteria"], list):
                return jsonify({"error": "criteria must be a list"}), 400
            if not data["criteria"]:
                return jsonify({"error": "criteria list cannot be empty"}), 400
            if not all(criterion in valid_criteria for criterion in data["criteria"]):
                return jsonify({"error": f"each criterion must be one of: {', '.join(valid_criteria)}"}), 400
        else:
            # Default to all criteria if none specified
            data["criteria"] = valid_criteria
        print(f"Valid optimization criteria: {data.get('criteria')}")

        # Call the model function to optimize the path
        response, status_code = optimize_patrol_path(str(path_object_id), data)
        print(f"Optimization response: {response}")

        if status_code == 200:
            # Log successful optimization
            app.logger.info(f"Successfully optimized path {path_id}")
            app.logger.info(f"Optimization stats: {response.get('optimization_stats', {})}")
            
            return jsonify({
                "message": "Path optimized successfully",
                "path_id": path_id,
                "optimization_result": response.get("optimization_result", {}),
                "optimization_stats": response.get("optimization_stats", {}),
                "applied_criteria": data["criteria"]
            }), 200
        else:
            return jsonify(response), status_code

    except Exception as e:
        app.logger.error(f"Error optimizing path: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Endpoint to retrieve all patrol paths for a specific robot
@app.route('/api/paths/<int:robot_id>', methods=['GET'])
def get_robot_paths(robot_id):
    response, status_code = get_paths_for_robot(robot_id)
    if status_code == 200 and not response:
        return jsonify({"message": f"No paths found for Robot ID {robot_id}"}), 404
    return jsonify(response), status_code

@app.route('/api/paths/<path_id>', methods=['DELETE'])
def delete_patrol_path_endpoint(path_id):
    """
    Deletes a patrol path by its ID.
    """
    try:
        # Call the model function to delete the path
        response, status_code = delete_patrol_path(path_id)
        return jsonify(response), status_code
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
