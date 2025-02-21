import time
import requests
import json
import concurrent.futures

# Base URL of the backend API
base_url = "http://localhost:5000/add_task"

# Function to add a task with retry logic
def add_task_with_retry(task, retries=5):
    headers = {'Content-Type': 'application/json'}
    data = {'task': task}
    for attempt in range(retries):
        try:
            response = requests.post(base_url, headers=headers, data=json.dumps(data))
            response.raise_for_status()  # Will raise an error for non-2xx status codes
            return response
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(2)  # Wait before retrying
            else:
                print("Max retries reached. Request failed.")
                return None

# Function to simulate a DoS attack by adding tasks in parallel
def simulate_dos_attack_parallel():
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        tasks = [f"Task #{i + 1}" for i in range(500)]
        futures = [executor.submit(add_task_with_retry, task) for task in tasks]
        
        for i, future in enumerate(futures):
            response = future.result()
            if response and response.status_code == 200:
                print(f"Task {i + 1} added successfully")
            else:
                print(f"Failed to add Task {i + 1}")

# Run the simulation
simulate_dos_attack_parallel()
