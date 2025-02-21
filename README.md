# Todo App with Kubernetes Horizontal Pod Autoscaling

## Overview
This repository contains a simple To-Do application with a frontend, backend, and database, deployed in a Kubernetes cluster with Horizontal Pod Autoscaling (HPA). Additionally, a Python script (`dos.py`) is included to simulate heavy requests and observe the pod autoscaling in action.

## Features
- **Frontend:** User interface to manage tasks.
- **Backend:** API for handling to-do list operations.
- **Database:** Stores to-do items persistently.
- **Kubernetes Deployment:** All components are containerized and deployed using Kubernetes.
- **Horizontal Pod Autoscaler (HPA):** Automatically scales the backend pods based on CPU usage.
- **Load Simulation (`dos.py`):** Generates high traffic to test autoscaling.

## Prerequisites
- Docker
- Kubernetes (Minikube, k3s, or any K8s cluster)
- Metrics Server deployed in cluster
- kubectl
- Helm (for database deployment, if required)
- Python (for running `dos.py`)


## Working
### Initial State
Before running the load test, there is only a single backend pod.

<img src="https://github.com/agrimpaneru/kubernetes-todo/blob/main/first.jpg" alt="Single backend pod" width="500px">

### Autoscaling in Action
After executing `dos.py`, the number of backend pods increases to handle the higher load.

<img src="image_url" alt="https://github.com/agrimpaneru/kubernetes-todo/blob/main/task.jpg" width="500px">

### Maximum Pod Scaling
As traffic continues, more pods are spawned dynamically.

<img src="https://github.com/agrimpaneru/kubernetes-todo/blob/main/11.jpg" alt="Increased number of pods" width="500px">

### CPU Threshold and Scaling Behavior
The CPU limit was set to **100m**, and once usage exceeded **50%**, a new pod was added. The maximum pod limit was configured to **10**.

<img src="https://github.com/agrimpaneru/kubernetes-todo/blob/main/33.jpg" alt="CPU threshold exceeded" width="500px">



