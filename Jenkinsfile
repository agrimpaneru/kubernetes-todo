pipeline {

    agent any

    

    environment {

        NAMESPACE = "todo-app"

        BUILD_TAG = "${BUILD_NUMBER}"

        KUBERNETES_TOKEN = credentials('Jekins') // Update with your actual credential ID

    }

    

    stages {

        stage('Checkout') {

            steps {

                checkout scm

            }

        }

        

        stage('Test') {

            steps {

                sh 'echo "Testing connectivity"'

            }

        }

    }

    

    post {

        failure {

            echo 'Pipeline failed'

        }

        success {

            echo 'Pipeline successful'

        }

    }

}
