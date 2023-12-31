pipeline {
    agent any // This tells Jenkins to run this pipeline on any available agent


    stages {
        stage('Build') {
            steps {
                // Build the Docker image
                script {
                    sh 'eval $(minikube docker-env)'
                    sh 'docker build -t flask-es-image:va employee_service/.'
                    sh 'docker build -t flask-ds-image:va department_service/.'
                    sh 'docker build -t flask-lms-image:va leave_management_service/.'
                    sh 'docker build -t ansible-image:va ansible_project/.'
                    sh 'docker build -t test:va .'
                }
            }
        }

        stage('Test') {
            steps {
                // Run tests inside your Docker container
                script {
                    sh 'docker run test:va'
                }
            }
        }

        stage('Deploy') {
            steps {
                // Deploy your application, adjust this to your deployment method
                script {
                    // Assuming you're using Kubernetes
                    sh 'kubectl apply -f kubernetes_project/es_deployment.yaml'
                    sh 'kubectl apply -f kubernetes_project/es_service.yaml'
                    sh 'kubectl apply -f kubernetes_project/ds_deployment.yaml'
                    sh 'kubectl apply -f kubernetes_project/ds_service.yaml'
                    sh 'kubectl apply -f kubernetes_project/lms_deployment.yaml'
                    sh 'kubectl apply -f kubernetes_project/lms_service.yaml'
                    sh 'kubectl apply -f kubernetes_project/ansible_deployment.yaml'
                    sh 'kubectl apply -f kubernetes_project/ansible_service.yaml'
                    
                }
            }
        }
    }
}
