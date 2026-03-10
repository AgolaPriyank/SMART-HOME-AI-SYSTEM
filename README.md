# IoT-Based Smart Home Automation with AI

This project is an industry-level implementation of an IoT-Based Smart Home Automation system using Artificial Intelligence. It simulates real-time sensor data, processes it via a Flask backend, and uses a Machine Learning model (Random Forest) to make automated decisions to control smart devices.

## Features
- **Real-time IoT Simulation:** Simulates Temperature, Humidity, Motion, and Light sensors.
- **RESTful API Backend:** Built with Flask to manage devices, receive sensor data, and serve historical logs.
- **AI-Driven Automation:** Scikit-learn Random Forest model trained to detect when to turn on/off devices based on sensor readings.
- **Interactive Dashboard:** Bootstrap 5 & Chart.js frontend for monitoring data and manual device control.
- **SQLite/MySQL Database Integration:** Robust tracking of sensor history and automation logs.

## Project Structure
- `backend/`: Flask API, database models, and routing.
- `backend/ml/`: Machine Learning model training and inference scripts.
- `frontend/`: HTML, CSS, and JS files for the dashboard UI.
- `simulator/`: Python script mimicking an ESP32 sending IoT data.
- `database/`: SQL schema for the database structure.

## Quick Start

### 1. Requirements
Ensure you have Python 3.8+ installed.

### 2. Setup Virtual Environment
```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Train the AI Model
Before running the server, the AI model needs to be generated:
```bash
python backend/ml/train.py
```
This generates synthetic historical data and trains the `model.pkl`.

### 5. Run the Application
You will need two terminal windows (both with the virtual environment activated).

**Terminal 1 (Backend Server):**
```bash
python backend/app.py
```
The dashboard will be available at `http://localhost:5000/`.

**Terminal 2 (IoT Simulator):**
```bash
python simulator/sensor_sim.py
```
This will start sending dummy sensor data to the backend API every few seconds.

## Database Note
By default, the application uses an SQLite database (`smarthome.db`) created automatically in the root or database folder for ease of setup. This can be switched to MySQL using the `database/schema.sql` by modifying `SQLALCHEMY_DATABASE_URI` in `backend/config.py`.
