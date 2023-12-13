# Backend-Devops-Lab

Project Overview: Backend DevOps Lab

A microservices-based backend system using Flask, orchestrated with Docker and Kubernetes, and integrated into a CI/CD pipeline with Jenkins and Ansible.

1. Microservices Development with Flask
Design Microservices: Plan the architecture and design of individual microservices (e.g., Employee, Department, Leave Management).
Develop RESTful APIs: Implement RESTful APIs for each microservice.
2. Unit Testing + Postman: Write and run unit tests for each service to ensure code quality and functionality.
3. Containerization with Docker
Create Dockerfiles: Write Dockerfiles for each microservice.
Docker Compose: Build images for your microservices and run containers using docker compose.
4. Configuration Management with Ansible
Write Ansible Playbooks: Automate environment setup and deployment tasks using Ansible.
Automate Deployments: Use Ansible for automated deployments to your Kubernetes cluster.
Local Testing: Run and test your containers locally.
5. Continuous Integration and Deployment with Jenkins
Setup Jenkins: Configure Jenkins for your project.
Build Pipeline: Create pipelines for automated building, testing, and deploying of your microservices.
Integrate with Source Control: Connect Jenkins to your Git repository.
6. Orchestration with Kubernetes
Kubernetes Manifests: Write Kubernetes manifests (YAML files) for deploying your microservices.
Deploy on Kubernetes: Deploy your microservices to a Kubernetes cluster (can be a local cluster like Minikube or a cloud-based one).
Test Orchestration: Ensure microservices are communicating effectively and are scalable.

---

**Steps to run code**

- Backend Flask Microservices: Run each microservice (3 of them) but navigating to the that microservice directory and running 'python3 <microservice_name>.py'
- Unit Tests: Run unit tests by navigating to root directory and running 'python3 -m unittest discover'

If you want to use docker:
- go to project root and type docker-compose up (will run the 3 microservices and one unit test service)
- you can do ctrl+c to stop the containers and then docker-compose down

---

**Learnings:**

- Docker:
    - The KEY difference in trying to make different services interact with each other, that wasnt caught in the react to flask communictaion from previous project, is that js loads onto browser and can fetch 'localhost' requests. However, in this project, containers cant talk to each other.

- Ansible:
    - Learnt the most here. Documented the files to explain in the places itself. However, will list what I learnt as I did. Refer to the ansible files to read along with the below points.
    1. inventory.txt: creating a group called local in inventory and then putting localhost with ansible_connection=local will work when testing but we need to change that to docker as we test the same out in containers.
    2. nginx.conf.j2: dont forget to put http:// before <container_name:port_name>.
    3. run_playbook.sh: running two playbooks and cant put both in CMD stanza in the dockerfile, so created a shell script and added both. Also added script to stop container from shutting after execution of playbook so I can leave it open for debugging.
    4. playbooks are quite self-explanatory. Was running into an issue with nginx reverse proxy, but I think it was because I hadnt written the script to start it before I was trying to reload it. Also, service module caused failure, so had to swtich to command module to run it, and that worked.
    5. Dockerfile: The step to install sudo is there because Ansible was failing at the become module. Maybe some issues with docker not having sudo baked in which ansible needs.  

---

WIP: 
Kubernetes, Jenkins