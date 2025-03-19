pipeline {
    agent any
    
    environment {
        NAMESPACE = "todo-app"
        BUILD_TAG = "${BUILD_NUMBER}"
        K8S_SERVER = "https://kubernetes.default.svc"  // Replace with your Kubernetes API server
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
                    sh """
                        sed -i 's|image:.*flask-app.*|image: flask-app:${BUILD_TAG}|g' K8/backend-deployment.yml
                        sed -i 's|image:.*todo-frontend.*|image: todo-frontend:${BUILD_TAG}|g' K8/frontend-deployment.yml
                        
                        # Add imagePullPolicy: Never
                        sed -i '/image: flask-app/a\\        imagePullPolicy: Never' K8/backend-deployment.yml
                        sed -i '/image: todo-frontend/a\\        imagePullPolicy: Never' K8/frontend-deployment.yml
                    """
                }
            }
        }
        
        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([string(credentialsId: 'kubeconfig-credential', variable: 'K8S_TOKEN')]) {
                    sh """
                        # Set kubectl context with the token
                        kubectl config set-cluster k8s --server=${K8S_SERVER}
                        kubectl config set-credentials jenkins --token=${K8S_TOKEN}
                        kubectl config set-context jenkins-context --cluster=k8s --user=jenkins --namespace=${NAMESPACE}
                        kubectl config use-context jenkins-context
                        
                        # Apply resources
                        kubectl apply -f K8/backend-deployment.yml -n ${NAMESPACE}
                        kubectl apply -f K8/backend-service.yml -n ${NAMESPACE}
                        kubectl apply -f K8/frontend-deployment.yml -n ${NAMESPACE}
                        kubectl apply -f K8/frontend-service.yml -n ${NAMESPACE}
                        
                        # Wait for deployments
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
