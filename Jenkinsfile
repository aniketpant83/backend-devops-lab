pipeline {
    agent any
    parameters {
        choice(name: 'ACTION', choices: ['deploy', 'delete'], description: 'Select the desired action for deployments')
    }


    stages {
        stage('Build') {
            steps {
                // Set docker env to minikube's and build the Docker image
                script {
                    if (params.ACTION == 'deploy'){
                        sh """
                        eval \$(minikube docker-env)
                        docker build -t flask-es-image:va employee_service/.
                        docker build -t flask-ds-image:va department_service/.
                        docker build -t flask-lms-image:va leave_management_service/.
                        docker build -t ansible-image:va ansible_project/.
                        """
                        sh 'docker build -t test:va .'
                }
                }
            }
        }

        stage('Test') {
            steps {
                // Run unittests inside test container
                script {
                    if (params.ACTION == 'deploy'){
                        sh 'docker run --name test-container test:va'
                    }
                }
            }
        }

        stage('Deploy/Delete') {
            steps {
                // Deploy your application, adjust this to your deployment method
                script {
                    if (params.ACTION == 'deploy'){
                    // Assuming you're using Kubernetes
                        sh 'kubectl apply -f kubernetes_project/es_deployment.yaml'
                        sh 'kubectl apply -f kubernetes_project/es_service.yaml'
                        sh 'kubectl apply -f kubernetes_project/ds_deployment.yaml'
                        sh 'kubectl apply -f kubernetes_project/ds_service.yaml'
                        sh 'kubectl apply -f kubernetes_project/lms_deployment.yaml'
                        sh 'kubectl apply -f kubernetes_project/lms_service.yaml'
                        sh 'kubectl apply -f kubernetes_project/ansible_deployment.yaml'
                        sh 'kubectl apply -f kubernetes_project/ansible_service.yaml'
                    } else if (params.ACTION == 'delete'){
                        sh 'kubectl delete deployment --all'
                        sh 'kubectl delete services --all'
                        sh """
                        eval \$(minikube docker-env)
                        docker rmi flask-es-image:va
                        docker rmi flask-ds-image:va
                        docker rmi flask-lms-image:va
                        docker rmi ansible-image:va
                        """
                        sh 'docker stop test-container'
                        sh 'docker rm test-container'
                        sh 'docker rmi test:va'

                    }
                }
            }
        }
    }
}
