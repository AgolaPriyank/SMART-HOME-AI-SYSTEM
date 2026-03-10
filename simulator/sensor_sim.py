import time
import random
import requests
import json

# URL of the Flask Backend
BACKEND_URL = "http://localhost:5000/api/sensors"

def simulate_environment():
    """Run an infinite loop simulating sensor data changes."""
    print("Starting IoT Sensor Simulator...")
    print(f"Target URL: {BACKEND_URL}")
    print("Press Ctrl+C to stop.")
    
    base_temp = 25.0
    base_hum = 50.0
    light_level = 800 # Daytime initially
    
    try:
        while True:
            # Simulate gradual changes
            temp = base_temp + random.uniform(-1.0, 1.0)
            hum = base_hum + random.uniform(-5.0, 5.0)
            
            # Simulate sudden events (motion)
            motion = random.choice([True, False, False, False]) # 25% chance of motion
            
            # Simulate day/night cycle or clouds
            if random.random() < 0.1:
                # Sudden change (e.g., someone turned off a light or sun set quickly)
                light_level = max(0, light_level - random.randint(100, 300))
            elif light_level < 200 and random.random() < 0.2:
                 light_level += random.randint(200, 500)
            else:
                 # Gradual change
                 light_level += random.randint(-50, 50)
                 
            light_level = max(0, min(1000, light_level)) # Keep within bounds
            
            payload = {
                "temperature": round(temp, 1),
                "humidity": round(hum, 1),
                "motion": motion,
                "light": round(light_level, 1) # Sending as float value (lux)
            }
            
            print(f"Sending data: {payload}")
            
            try:
                headers = {'Content-type': 'application/json'}
                response = requests.post(BACKEND_URL, data=json.dumps(payload), headers=headers)
                
                if response.status_code == 201:
                    result = response.json()
                    if result.get('ai_action_taken'):
                        print(f"AI Action Triggered: {result['message']}")
                    else:
                        print("Data accepted.")
                else:
                    print(f"Server Error {response.status_code}: {response.text}")
                    
            except requests.exceptions.ConnectionError:
                print("Connection failed. Is the backend running?")
                
            # Wait before next tick
            time.sleep(10)
            
    except KeyboardInterrupt:
        print("\nSimulator stopped by user.")

if __name__ == "__main__":
    simulate_environment()
