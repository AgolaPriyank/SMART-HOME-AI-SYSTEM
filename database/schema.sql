CREATE DATABASE IF NOT EXISTS smarthome_db;
USE smarthome_db;

-- Table for Devices
CREATE TABLE IF NOT EXISTS Devices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(100),
    status ENUM('ON', 'OFF') DEFAULT 'OFF',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for Sensor Data
CREATE TABLE IF NOT EXISTS SensorData (
    id INT AUTO_INCREMENT PRIMARY KEY,
    temperature FLOAT,
    humidity FLOAT,
    motion BOOLEAN,
    light VARCHAR(50),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for Automation Logs
CREATE TABLE IF NOT EXISTS AutomationLogs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    device_id INT,
    action VARCHAR(50),
    trigger_type ENUM('Manual', 'AI') DEFAULT 'Manual',
    confidence_score FLOAT DEFAULT 0.0,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (device_id) REFERENCES Devices(id)
);

-- Insert dummy devices for testing
INSERT INTO Devices (name, type) VALUES ('Living Room Light', 'Light');
INSERT INTO Devices (name, type) VALUES ('AC', 'Appliance');
INSERT INTO Devices (name, type) VALUES ('Main Door Lock', 'Security');
