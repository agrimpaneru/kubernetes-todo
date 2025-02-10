# Dockerized-Todo with Kubernetes

This is a simple, Kubernetes-deployed To-Do List application using Flask for the backend, MySQL for the database, and Nginx for serving the frontend.

## Project Structure

```
.
├── backend
│   ├── backend.py         # Flask backend application
│   ├── requirements.txt   # Python dependencies
│   ├── Dockerfile         # Dockerfile for Flask app
├── frontend
│   ├── index.html         # Frontend HTML file
│   ├── Dockerfile         # Dockerfile for Nginx
├── k8s
│   ├── backend-deployment.yaml   # Backend deployment config
│   ├── backend-service.yaml      # Backend service config
│   ├── db-deployment.yaml        # MySQL database deployment
│   ├── db-service.yaml           # MySQL service config
│   ├── frontend-service.yaml     # Frontend service config
├── README.md              # Project documentation
```

## Features

- Add tasks to the to-do list
- View all tasks
- Delete tasks
- Kubernetes-deployed for scalability and resilience
- Uses MySQL for data persistence

## Prerequisites

- Docker installed
- Kubernetes (Minikube, K3s, or a cloud Kubernetes service)
- kubectl installed and configured

## Getting Started

### 1. Clone the Repository

```sh
git clone https://github.com/your-username/dockerized-todo.git
cd dockerized-todo
```

### 2. Build and Push Docker Images

```sh
docker build -t backend:latest ./backend
```

Tag and push the image to a container registry if necessary (e.g., Docker Hub or a private registry).

### 3. Deploy to Kubernetes

Apply the Kubernetes manifests:

```sh
kubectl apply -f k8s/
```

### 4. Verify Deployments

Check the status of the Pods and Services:

```sh
kubectl get pods
kubectl get services
```

### 5. Access the Application

- **Backend API:** `http://<NODE_IP>:<NODE_PORT>/`
- **Frontend:** `http://<NODE_IP>:30000`
- **MySQL Database:** Accessible internally via `db-service:3306`

### Port Forwarding (for WSL Users)
```sh
kubectl port-forward <frontend-pod-name> 8000:80
kubectl port-forward <backend-pod-name> 5000:5000
```

## API Endpoints

### 1. Add a Task

**Endpoint:** `POST /add_task`

```json
{
  "task": "Buy groceries"
}
```

### 2. Get All Tasks

**Endpoint:** `GET /get_tasks`

### 3. Delete a Task

**Endpoint:** `DELETE /delete_task/{task_id}`

## Stopping the Application

To delete all deployed services and deployments, run:

```sh
kubectl delete -f k8s/
```



