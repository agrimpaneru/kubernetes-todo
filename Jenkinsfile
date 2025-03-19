pipeline {
    agent any

    environment {
        NAMESPACE = "todo-app"
        BUILD_TAG = "${BUILD_NUMBER}"
        KUBERNETES_TOKEN = credentials('jenkins-secret')
    }

    stages {
        stage('Start Minikube') {
            steps {
                script {
                    sh """
                        set -x
                        
                        # Check if Minikube is running
                        if ! minikube status >/dev/null 2>&1; then
                            echo "Starting Minikube..."
                            minikube start --driver=docker
                        else
                            echo "Minikube is already running."
                        fi
                    """
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    sh """
                        set -x
                        
                        # Get Minikube IP
                        SERVER_IP=\$(minikube ip)
                        echo "Using Minikube IP: \$SERVER_IP"
                        
                        # Ensure Kubernetes token is available
                        if [[ -z "\$KUBERNETES_TOKEN" ]]; then
                            echo "ERROR: Kubernetes token is empty!"
                            exit 1
                        fi

                        # Create a temporary kubeconfig file
                        KUBECONFIG_FILE=\$(mktemp)
                        
                        cat > \$KUBECONFIG_FILE << EOF
apiVersion: v1
kind: Config
clusters:
- name: minikube
  cluster:
    server: https://\$SERVER_IP:8443
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
                        
                        export KUBECONFIG=\$KUBECONFIG_FILE
                        
                        # Deploy to Kubernetes
                        kubectl apply -f K8/backend-deployment.yml -n ${NAMESPACE} --validate=false
                        kubectl apply -f K8/frontend-deployment.yml -n ${NAMESPACE} --validate=false
                        
                        # Clean up kubeconfig
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
