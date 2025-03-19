pipeline {
    agent any
    
    environment {
        NAMESPACE = "jenkins"
        // Using Minikube's built-in Docker daemon
        MINIKUBE_IP = sh(script: 'minikube ip', returnStdout: true).trim()
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Connect to Minikube Docker') {
            steps {
                // This allows Jenkins to use Minikube's Docker daemon
                sh '''
                    eval $(minikube -p minikube docker-env)
                    docker ps
                '''
            }
        }
        
        stage('Build Docker Images') {
            steps {
                script {
                    // Build images directly in Minikube's Docker daemon
                    sh '''
                        # Build backend image
                        docker build -t flask-app:${BUILD_NUMBER} ./backend
                        
                        # Build frontend image
                        docker build -t todo-frontend:${BUILD_NUMBER} ./frontend
                    '''
                }
            }
        }
        
        stage('Update Kubernetes Manifests') {
            steps {
                script {
                    // Update deployment files with current build image tags
                    sh '''
                        sed -i 's|image:.*flask-app.*|image: flask-app:${BUILD_NUMBER}|g' K8/backend-deployment.yml
                        sed -i 's|image:.*todo-frontend.*|image: todo-frontend:${BUILD_NUMBER}|g' K8/frontend-deployment.yml
                        
                        # Important: Add imagePullPolicy: Never to deployment files
                        sed -i '/image: flask-app/a\\        imagePullPolicy: Never' K8/backend-deployment.yml
                        sed -i '/image: todo-frontend/a\\        imagePullPolicy: Never' K8/frontend-deployment.yml
                    '''
                }
            }
        }
        
        stage('Deploy to Minikube') {
            steps {
                script {
                    sh '''
                        # Create namespace if it doesn't exist
                        kubectl create namespace ${NAMESPACE} --dry-run=client -o yaml | kubectl apply -f -
                        
                        # Apply backend resources
                        kubectl apply -f K8/backend-deployment.yml -n ${NAMESPACE}
                        kubectl apply -f K8/backend-service.yml -n ${NAMESPACE}
                        
                        # Apply frontend resources
                        kubectl apply -f K8/frontend-deployment.yml -n ${NAMESPACE}
                        kubectl apply -f K8/frontend-service.yml -n ${NAMESPACE}
                        
                        # Wait for deployments to be ready
                        kubectl rollout status deployment/flask-app -n ${NAMESPACE} --timeout=180s
                        kubectl rollout status deployment/todo-frontend -n ${NAMESPACE} --timeout=180s
                    '''
                }
            }
        }
        
        stage('Display Service URLs') {
            steps {
                script {
                    sh '''
                        echo "Backend URL: $(minikube service flask-app -n ${NAMESPACE} --url)"
                        echo "Frontend URL: $(minikube service todo-frontend -n ${NAMESPACE} --url)"
                    '''
                }
            }
        }
    }
    
    post {
        failure {
            echo 'Deployment to Minikube failed'
        }
        success {
            echo 'Deployment to Minikube successful'
        }
    }
}
