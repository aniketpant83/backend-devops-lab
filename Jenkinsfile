pipeline {
    agent any // This tells Jenkins to run this pipeline on any available agent

    environment {
        // Define environment variables here
        DOCKER_IMAGE_ES = "flask-es-image:va"
        DOCKER_IMAGE_DS = "flask-ds-image:va"
        DOCKER_IMAGE_LMS = "flask-lms-image:va"
        DOCKER_IMAGE_ANSIBLE = "flask-ansible-image:va"
        DOCKER_IMAGE_TEST = "flask-test-image:va"
    }

    stages {
        stage('Build') {
            steps {
                // Build the Docker image
                script {
                    docker.build "${env.DOCKER_IMAGE_ES}"
                    docker.build "${env.DOCKER_IMAGE_DS}"
                    docker.build "${env.DOCKER_IMAGE_LMS}"
                    docker.build "${env.DOCKER_IMAGE_ANSIBLE}"
                    docker.build "${env.DOCKER_IMAGE_TEST}"
                }
            }
        }

        stage('Test') {
            steps {
                // Run tests inside your Docker container
                script {
                    docker.run("${env.DOCKER_IMAGE_TEST}", "pytest")
                }
            }
        }

        stage('Deploy') {
            steps {
                // Deploy your application, adjust this to your deployment method
                script {
                    // Assuming you're using Kubernetes
                    sh 'kubectl apply -f es_deployment.yaml'
                    sh 'kubectl apply -f es_service.yaml'
                    sh 'kubectl apply -f ds_deployment.yaml'
                    sh 'kubectl apply -f ds_service.yaml'
                    sh 'kubectl apply -f lms_deployment.yaml'
                    sh 'kubectl apply -f lms_service.yaml'
                    sh 'kubectl apply -f ansible_deployment.yaml'
                    sh 'kubectl apply -f ansible_service.yaml'
                    
                }
            }
        }
    }

    post {
        always {
            // Clean up after the pipeline is done
            script {
                docker.rmi("${env.DOCKER_IMAGE_ES}")
                docker.rmi("${env.DOCKER_IMAGE_DS}")
                docker.rmi("${env.DOCKER_IMAGE_LMS}")
                docker.rmi("${env.DOCKER_IMAGE_ANSIBLE}")
                docker.rmi("${env.DOCKER_IMAGE_TEST}")
            }
        }

        success {
            // Actions to take on success
            echo 'Build, Test and Deployment stages succeeded!'
        }

        failure {
            // Actions to take on failure
            echo 'The pipeline failed!'
        }
    }
}
