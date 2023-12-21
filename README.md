# Backend-Devops-Lab

Project Overview: Backend DevOps Lab

A microservices-based backend system using Flask, orchestrated with Docker and Kubernetes, and integrated into a CI/CD pipeline with Jenkins and Ansible.

1. Microservices Development with Flask
    - Designed individual microservices (Employee, Department, Leave Management).
    - Developed RESTful APIs for each microservice.
    - Used SQLAlechmy to handle DB.
2. Testing 
    - Wrote unittests for automated testing of Flask microservices.
    - Postman for manual testing of APIs
3. Containerization with Docker
    - Created 5 Dockerfiles: 1 for each microservice, 1 for unittests, and 1 for ansible (explain in next step)
    - A final docker compose file.
4. Configuration Management with Ansible: Wrote Ansible Playbooks to: 
    - Automate testing of microservices being up and running.
    - Automate set-up of Nginx reverse proxy.
    - As indicated in the previous point, created a Dockerfile for this too, and added to docker compose.
5. WIP: Continuous Integration and Deployment with Jenkins
6. WIP: Orchestration with Kubernetes
7. WIP: Prometheus and Grafana
---

**Steps to run code**

- Clone repo to a directory and open on VSCode or editor of choice.
- Install Docker (and if needed, other things too) and run 'docker compose up' from project root directory
- This will run the 3 microservices, unit tests for all 3, and ansible playbooks.
- Use to ctrl+c to stop the containers and then docker-compose down to delete containers. Remember to delete images for cleanup
- Expected result of unit tests should be 17 tests running and passing, and ansible playbook with 8 oks and 7 changed, 0 fails.
- Kubernetes:
    - Install kubectl and minikube, and check if kubectl config points to minikube.
    - Build each image separately in the minikube docker env.
    - write and run deployments + svcs.
    - access apps running on cluster from original host using minikube cluster ip with port given by minikube in terminal.
    - if want to test from one conatiner to another, just do curl servicename:portname

---

**Learnings:**

- Docker:
    - The KEY difference in trying to make different services interact with each other, that wasnt caught in the react to flask communictaion from previous project, is that js loads onto browser and can fetch 'localhost' requests. However, in this project, containers cant talk to each other.


- Ansible:
    Learnt the most here. Documented the files to explain in the places itself. However, will list what I learnt as I did. Refer to the ansible files to read along with the below points.
    1. inventory.txt: creating a group called local in inventory and then putting localhost with ansible_connection=local will work when testing but we need to change that to docker as we test the same out in containers.
    2. nginx.conf.j2: dont forget to put http:// before <container_name:port_name>. example: http://employee_portal_pp-employee_service-1:5001;
    3. run_playbook.sh: running two playbooks and cant put both in CMD stanza in the dockerfile, so created a shell script and added both. Also added script to stop container from shutting after execution of playbook so I can leave it open for debugging.
    4. playbooks are quite self-explanatory. Was running into an issue with nginx reverse proxy, but I think it was because I hadnt written the script to start it before I was trying to reload it. Also, service module caused failure, so had to swtich to command module to run it, and that worked.
    5. Dockerfile: The step to install sudo is there because Ansible was failing at the become module. Maybe some issues with docker not having sudo baked in which ansible needs.  
    6. Kubernetes: Explained in the kubernetes section.
    7. the ansible_connection=<insert> tells ansible whether to run thigns locally, or ssh into something or docker etc.

---

WIP: 
Kubernetes, Jenkins

---

***Documenting My Kubernetes Experience***

Kubernetes is used for container orchestration. When we do docker compose, it just deploys once container per image. If that fails, it does not redeploy, it does not scale the number of containers according to traffice, it does not provide load balancing and many other features, all of which is provided by Kubernetes.

- You need to set docker daemon to the one in minikube because docker checks your system docker instead of the container docker. eval $(minikube docker-env) to set it to minikube docker and eval $(minikube docker-env -u) to unset it backt o host. Node Port is what we, the external party, accesses it from.  
- Till now I was deploying the app on docker compose up, now we just build each image separately from the dockerfile using 'docker build -t <image_name_in_my_deployment> .' Important to build images in the minikube docker env and not in host docker.
- Next, write your manifests. We need one for deployment and one for service. Do this for how many every microservices you want to deploy. 
- in the service manifest, there are three types of ports we are writing. It is essential to understand what each port is for. Nodeport is for external access, port is for what all services in cluster will talk using, target port is what service uses for load balancing.
- Once deployments and services are deployed, can use url generated by 'minikube service <service_name> --url' to access the same.
- Enter a pod using kubectl exec -it <podName> -- /bin/bash
- You can access other services from a container using curl <service_name>:<port number (5001 for eg)>
- trying to get nginx to reverse proxy for all three flask apps with different location pathings didnt work. So, had to stick to just employee_service as reverse proxying. 

---