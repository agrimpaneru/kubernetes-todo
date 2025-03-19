pipeline {
    agent any
    
    environment {
        NAMESPACE = "todo-app"
        BUILD_TAG = "${BUILD_NUMBER}"
        // Reference the credential ID where you stored the token
        KUBERNETES_TOKEN = credentials('Jekins') // Replace with your actual credential ID
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
               script {
                    sh """
                        # Create a temporary kubeconfig file
                        KUBECONFIG_FILE=\$(mktemp)
                        
                        # Create kubeconfig with token authentication
                        cat > \$KUBECONFIG_FILE << EOF
apiVersion: v1
kind: Config
clusters:
- name: minikube
  cluster:
    server: \$(minikube ip):8443
    insecure-skip-tls-verify: true
users:
- name: jenkins
  user:
    token: \${KUBERNETES_TOKEN}
contexts:
- context:
    cluster: minikube
    user: jenkins
    namespace: ${NAMESPACE}
  name: jenkins-minikube
current-context: jenkins-minikube
EOF
                        
                        # Use the temporary kubeconfig
                        export KUBECONFIG=\$KUBECONFIG_FILE
                        
                        # Make sure namespace exists
                        kubectl create namespace ${NAMESPACE} --dry-run=client -o yaml | kubectl apply -f -
                        
                        # Apply resources 
                        kubectl apply -f K8/backend-deployment.yml -n ${NAMESPACE} --validate=false
                        kubectl apply -f K8/backend-service.yml -n ${NAMESPACE} --validate=false
                        kubectl apply -f K8/frontend-deployment.yml -n ${NAMESPACE} --validate=false
                        kubectl apply -f K8/frontend-service.yml -n ${NAMESPACE} --validate=false
                        
                        # Wait for deployments
                        kubectl rollout status deployment/flask-app -n ${NAMESPACE} --timeout=180s
                        kubectl rollout status deployment/todo-frontend -n ${NAMESPACE} --timeout=180s
                        
                        # Clean up temporary kubeconfig
                        rm -f \$KUBECONFIG_FILE
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
