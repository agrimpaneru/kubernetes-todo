pipeline {
    agent any
    
    environment {
        NAMESPACE = "todo-app"
        BUILD_TAG = "${BUILD_NUMBER}"
        KUBECONFIG = credentials('kubeconfig-credential') // Your Jenkins credential containing kubeconfig
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build Docker Images') {
            steps {
                script {
                    // Build images locally
                    sh """
                        # Build backend image
                        docker build -t flask-app:${BUILD_TAG} ./backend
                        
                        # Build frontend image
                        docker build -t todo-frontend:${BUILD_TAG} ./frontend
                    """
                }
            }
        }
        
        stage('Update Kubernetes Manifests') {
            steps {
                script {
                    // Update deployment files with current build image tags
                    sh """
                        sed -i 's|image:.*flask-app.*|image: flask-app:${BUILD_TAG}|g' K8/backend-deployment.yml
                        sed -i 's|image:.*todo-frontend.*|image: todo-frontend:${BUILD_TAG}|g' K8/frontend-deployment.yml
                        
                        # Make sure imagePullPolicy is set to Never
                        sed -i '/image: flask-app/a\\        imagePullPolicy: Never' K8/backend-deployment.yml
                        sed -i '/image: todo-frontend/a\\        imagePullPolicy: Never' K8/frontend-deployment.yml
                    """
                }
            }
        }
        
        stage('Deploy to Kubernetes') {
            steps {
                script {
                    sh """
                        export KUBECONFIG=${KUBECONFIG}
                        
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
                    """
                }
            }
        }
    }
    
    post {
        failure {
            echo 'Deployment to Kubernetes failed'
        }
        success {
            echo 'Deployment to Kubernetes successful'
        }
    }
}
