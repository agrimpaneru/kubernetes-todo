import requests
import json

# Base URL of the backend API
base_url = "http://localhost:5000/add_task"

# Function to add a task
def add_task(task):
    headers = {'Content-Type': 'application/json'}
    data = {'task': task}
    response = requests.post(base_url, headers=headers, data=json.dumps(data))
    return response

# Simulate adding 100 tasks
def simulate_dos_attack():
    for i in range(10000):
        task = f"Task #{i + 1}"
        response = add_task(task)
        if response.status_code == 200:
            print(f"Task {i + 1} added successfully")
        else:
            print(f"Failed to add Task {i + 1}: {response.status_code}")

# Run the simulation
simulate_dos_attack()
