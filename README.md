# backend-devops-lab

Project Overview: Backend DevOps Lab
A microservices-based backend system using Flask, orchestrated with Docker and Kubernetes, and integrated into a CI/CD pipeline with Jenkins and Ansible.

1. Microservices Development with Flask
Design Microservices: Plan the architecture and design of individual microservices (e.g., Employee, Department, Leave Management).
Develop RESTful APIs: Implement RESTful APIs for each microservice.
Unit Testing: Write and run unit tests for each service to ensure code quality and functionality.
2. Containerization with Docker
Create Dockerfiles: Write Dockerfiles for each microservice.
Build Docker Images: Build images for your microservices.
Local Testing: Run and test your containers locally.
3. Orchestration with Kubernetes
Kubernetes Manifests: Write Kubernetes manifests (YAML files) for deploying your microservices.
Deploy on Kubernetes: Deploy your microservices to a Kubernetes cluster (can be a local cluster like Minikube or a cloud-based one).
Test Orchestration: Ensure microservices are communicating effectively and are scalable.
4. Continuous Integration and Deployment with Jenkins
Setup Jenkins: Configure Jenkins for your project.
Build Pipeline: Create pipelines for automated building, testing, and deploying of your microservices.
Integrate with Source Control: Connect Jenkins to your Git repository.
5. Configuration Management with Ansible
Write Ansible Playbooks: Automate environment setup and deployment tasks using Ansible.
Automate Deployments: Use Ansible for automated deployments to your Kubernetes cluster.

---

Steps to run code:

- Backend Flask Microservices: Run each microservice (3 of them) but navigating to the that microservice directory and running 'python3 <microservice_name>.py'
- Unit Tests: Run unit tests by navigating to root directory and running 'python3 -m unittest discover'

If you want to use docker:
- go to project root and type docker-compose up (will run the 3 microservices and one unit test service)
- you can do ctrl+c to stop the containers and then docker-compose down

---

WIP: 
Docker, kubernetes, Ansible, Jenkins, Reverse Proxy