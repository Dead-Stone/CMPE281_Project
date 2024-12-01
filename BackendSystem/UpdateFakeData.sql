
-- Insert data into 'owners' table
INSERT INTO owners (name, email, contact_info, created_at)
VALUES
('John Smith', 'john.smith@example.com', '123-456-7890', '2024-01-01 10:00:00'),
('Jane Doe', 'jane.doe@example.com', '234-567-8901', '2024-01-02 11:00:00'),
('Alice Johnson', 'alice.johnson@example.com', '345-678-9012', '2024-01-03 12:00:00'),
('Robert Brown', 'robert.brown@example.com', '456-789-0123', '2024-01-04 13:00:00'),
('Emily White', 'emily.white@example.com', '567-890-1234', '2024-01-05 14:00:00');

-- Insert data into 'system_staff' table
INSERT INTO system_staff (name, role, contact_info, created_at)
VALUES
('Michael Scott', 'Security Engineer', '678-901-2345', '2024-02-01 15:00:00'),
('Dwight Schrute', 'Technician', '789-012-3456', '2024-02-02 16:00:00'),
('Pam Beesly', 'Manager', '890-123-4567', '2024-02-03 17:00:00'),
('Jim Halpert', 'Operator', '901-234-5678', '2024-02-04 18:00:00'),
('Stanley Hudson', 'Technician', '012-345-6789', '2024-02-05 19:00:00');

-- Insert data into 'robots' table
INSERT INTO robots (owner_id, assigned_staff_id, name, model, created_at)
VALUES
(1, 1, 'SecurityBot Alpha', 'Model A', '2024-03-01 08:00:00'),
(2, 2, 'GuardBot Beta', 'Model B', '2024-03-02 09:00:00'),
(3, 3, 'PatrolBot Gamma', 'Model C', '2024-03-03 10:00:00'),
(4, 4, 'MonitorBot Delta', 'Model D', '2024-03-04 11:00:00'),
(5, 5, 'AlertBot Epsilon', 'Model E', '2024-03-05 12:00:00');

-- Insert data into 'robot_status' table
INSERT INTO robot_status (robot_id, status, location, battery_level, temperature, timestamp)
VALUES
(1, 'Active', 'Warehouse A', 85, 36.5, '2024-04-01 13:00:00'),
(2, 'Inactive', 'Main Gate', 50, 38.0, '2024-04-02 14:00:00'),
(3, 'Under Maintenance', 'Control Room', 30, 37.2, '2024-04-03 15:00:00'),
(4, 'Decommissioned', 'Storage Area', 10, 35.8, '2024-04-04 16:00:00'),
(5, 'Active', 'Patrol Route B', 95, 36.1, '2024-04-05 17:00:00');

-- Insert data into 'patrol_schedules' table
INSERT INTO patrol_schedules (robot_id, staff_id, start_time, end_time, path_details, created_at)
VALUES
(1, 1, '2024-05-01 08:00:00', '2024-05-01 10:00:00', 'Patrol around Warehouse A', '2024-05-01 07:30:00'),
(2, 2, '2024-05-02 09:00:00', '2024-05-02 11:00:00', 'Monitor Main Gate and surrounding area', '2024-05-02 08:30:00'),
(3, 3, '2024-05-03 12:00:00', '2024-05-03 14:00:00', 'Routine check in Control Room', '2024-05-03 11:30:00'),
(4, 4, '2024-05-04 15:00:00', '2024-05-04 17:00:00', 'Inspect Storage Area', '2024-05-04 14:30:00'),
(5, 5, '2024-05-05 18:00:00', '2024-05-05 20:00:00', 'Patrol Route B for security threats', '2024-05-05 17:30:00');

-- Insert data into 'service_alerts' table
INSERT INTO service_alerts (robot_id, staff_id, alert_type, alert_time, description)
VALUES
(1, 1, 'Unauthorized Access Attempt', '2024-06-01 14:23:00', 'Multiple failed access attempts detected. Possible brute-force attack on security systems.'),
(2, 2, 'Sensor Tampering Detected', '2024-06-02 09:45:00', 'External sensors report physical tampering. Potential sabotage detected.'),
(3, 3, 'Critical Battery Failure', '2024-06-03 17:30:00', 'Battery levels critically low. System integrity at risk, immediate recharge required.'),
(4, 4, 'Connection Lost - Possible Jamming', '2024-06-04 11:15:00', 'Network connection lost. Possible signal jamming or interference detected in the area.'),
(5, 5, 'Unexpected Shutdown - Potential Security Breach', '2024-06-05 22:50:00', 'Robot experienced an unexpected shutdown. Security breach suspected, further investigation needed.'),
(1, 2, 'Data Integrity Compromised', '2024-06-06 03:20:00', 'Data logs show signs of unauthorized modification. Security integrity compromised.'),
(2, 3, 'Unauthorized Movement Detected', '2024-06-07 13:10:00', 'Robot moved without authorization. Potential remote hijacking or malfunction.'),
(3, 4, 'Camera Obscured or Disabled', '2024-06-08 08:40:00', 'Camera vision obstructed or disabled. Manual inspection required.'),
(4, 5, 'High Temperature Detected - Possible Fire Hazard', '2024-06-09 16:05:00', 'Temperature sensors report abnormally high levels. Fire hazard suspected, immediate response needed.'),
(5, 1, 'Unauthorized Access Attempt', '2024-06-10 19:55:00', 'Multiple failed access attempts detected. Possible brute-force attack on security systems.');

-- Insert data into 'simulation_logs' table
INSERT INTO simulation_logs (robot_id, simulation_config, start_time, end_time, result)
VALUES
(1, 'Test Config Alpha', '2024-07-01 10:00:00', '2024-07-01 12:00:00', 'Simulation successful with minor errors.'),
(2, 'Test Config Beta', '2024-07-02 11:00:00', '2024-07-02 13:00:00', 'Simulation completed successfully. No issues detected.'),
(3, 'Test Config Gamma', '2024-07-03 14:00:00', '2024-07-03 16:00:00', 'Simulation failed due to battery drain.'),
(4, 'Test Config Delta', '2024-07-04 15:00:00', '2024-07-04 17:00:00', 'Simulation interrupted. Connection lost.'),
(5, 'Test Config Epsilon', '2024-07-05 18:00:00', '2024-07-05 20:00:00', 'Simulation completed with warnings. Temperature spike detected.');

-- Insert data into 'images' table
INSERT INTO images (robot_id, sensor_id, image_url, timestamp)
VALUES
(1, 'temp-sensor-001', 'http://example.com/images/robot1_sensor1.jpg', '2024-08-01 08:00:00'),
(2, 'motion-sensor-002', 'http://example.com/images/robot2_sensor2.jpg', '2024-08-02 09:00:00'),
(3, 'camera-sensor-003', 'http://example.com/images/robot3_sensor3.jpg', '2024-08-03 10:00:00'),
(4, 'infrared-sensor-004', 'http://example.com/images/robot4_sensor4.jpg', '2024-08-04 11:00:00'),
(5, 'gps-sensor-005', 'http://example.com/images/robot5_sensor5.jpg', '2024-08-05 12:00:00');