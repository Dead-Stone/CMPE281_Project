
CREATE DATABASE IF NOT EXISTS project;
USE project;

-- Table: owners
CREATE TABLE owners (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    contact_info VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: system_staff
CREATE TABLE system_staff (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    role VARCHAR(100) NOT NULL,
    contact_info VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: robots
CREATE TABLE robots (
    id INT AUTO_INCREMENT PRIMARY KEY,
    owner_id INT,
    assigned_staff_id INT,
    name VARCHAR(255) NOT NULL,
    model VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES owners(id),
    FOREIGN KEY (assigned_staff_id) REFERENCES system_staff(id)
);

-- Table: robot_status
CREATE TABLE robot_status (
    id INT AUTO_INCREMENT PRIMARY KEY,
    robot_id INT NOT NULL,
    status VARCHAR(100) NOT NULL,
    location VARCHAR(255),
    battery_level INT,
    temperature DECIMAL(5, 2),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (robot_id) REFERENCES robots(id)
);

-- Table: patrol_schedules
CREATE TABLE patrol_schedules (
    id INT AUTO_INCREMENT PRIMARY KEY,
    robot_id INT NOT NULL,
    staff_id INT NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    path_details TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (robot_id) REFERENCES robots(id),
    FOREIGN KEY (staff_id) REFERENCES system_staff(id)
);

-- Table: service_alerts
CREATE TABLE service_alerts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    robot_id INT NOT NULL,
    staff_id INT,
    alert_type VARCHAR(100) NOT NULL,
    severity VARCHAR(50) DEFAULT 'low',
    alert_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT,
    FOREIGN KEY (robot_id) REFERENCES robots(id),
    FOREIGN KEY (staff_id) REFERENCES system_staff(id)
);


-- Table: simulation_logs
CREATE TABLE simulation_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    robot_id INT NOT NULL,
    simulation_config TEXT,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    result TEXT,
    FOREIGN KEY (robot_id) REFERENCES robots(id)
);

-- Table: images
CREATE TABLE images (
    id INT AUTO_INCREMENT PRIMARY KEY,
    robot_id INT NOT NULL,
    sensor_id VARCHAR(255),
    image_url VARCHAR(255),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (robot_id) REFERENCES robots(id)
);

-- MongoDB Collections are typically created dynamically by the application, 
-- but here is how they would be structured in a SQL-like format:

-- Collection: alert_logs (Equivalent MongoDB Structure)
-- {
--     "_id": ObjectId,
--     "robot_id": Integer,
--     "alert_type": String,
--     "severity": String,
--     "timestamp": ISODate,
--     "metadata": Object
-- }

-- Collection: sensors (Equivalent MongoDB Structure)
-- {
--     "_id": ObjectId,
--     "robot_id": Integer,
--     "sensor_type": String,
--     "readings": Object,
--     "timestamp": ISODate
-- }

-- Collection: simulation_data (Equivalent MongoDB Structure)
-- {
--     "_id": ObjectId,
--     "robot_id": Integer,
--     "simulation_config": Object,
--     "start_time": ISODate,
--     "end_time": ISODate,
--     "result": String
-- }
