# Backend-Devops-Lab

Project Overview: Backend DevOps Lab

A microservices-based backend system using Flask (Tested with unittests and Postman), Ansible, Nginx Reverse Proxy, orchestrated with Docker and Kubernetes, monitored using Prometheus & Grafana, and integrated into a CI/CD pipeline with Jenkins.

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
5. Orchestration with Kubernetes
    - Created deployments + nodeport type services for 3 flask microservices and the ansible playboooks.
    - Had to reconfigure nginx settings to go from docker enviornment to minikube set-up.
6. Prometheus and Grafana
    - Used prom & grafana helm charts to scrape and visualize metrics from the department service.
7. WIP: Continuous Integration and Deployment with Jenkins
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

***Docker: Images + Compose***
    - The KEY difference in trying to make different services interact with each other, that wasnt caught in the react to flask communictaion from previous project, is that js loads onto browser and can fetch 'localhost' requests. However, in this project, containers cant talk to each other.

***Ansible: Nginx Reverse Proxy***
    Learnt the most here. Documented the files to explain in the places itself. However, will list what I learnt as I did. Refer to the ansible files to read along with the below points.
    1. inventory.txt: creating a group called local in inventory and then putting localhost with ansible_connection=local will work when testing but we need to change that to docker as we test the same out in containers.
    2. nginx.conf.j2: dont forget to put http:// before <container_name:port_name>. example: http://employee_portal_pp-employee_service-1:5001;
    3. run_playbook.sh: running two playbooks and cant put both in CMD stanza in the dockerfile, so created a shell script and added both. Also added script to stop container from shutting after execution of playbook so I can leave it open for debugging.
    4. playbooks are quite self-explanatory. Was running into an issue with nginx reverse proxy, but I think it was because I hadnt written the script to start it before I was trying to reload it. Also, service module caused failure, so had to swtich to command module to run it, and that worked.
    5. Dockerfile: The step to install sudo is there because Ansible was failing at the become module. Maybe some issues with docker not having sudo baked in which ansible needs.  
    6. Kubernetes part of ansible is explained in the kubernetes section.
    7. the ansible_connection=<insert> tells ansible whether to run thigns locally, or ssh into something or docker etc.

***Kubernetes: Minikube***

Kubernetes is used for container orchestration. When we do docker compose, it just deploys once container per image. If that fails, it does not redeploy, it does not scale the number of containers according to traffic, it does not provide load balancing and many other features, all of which are provided by Kubernetes.

- You need to set docker daemon to the one in minikube because docker checks your system docker instead of the container docker. eval $(minikube docker-env) to set it to minikube docker and eval $(minikube docker-env -u) to unset it back to host. Node Port is what we, the external party, accesses it from.  
- Till now I was deploying the app on docker compose up, now we just build each image separately from the dockerfile using 'docker build -t <image_name_in_my_deployment> .' Important to build images in the minikube docker env and not in host docker.
- Next, write your manifests. We need one for deployment and one for service. Do this for how many every microservices you want to deploy. 
- in the service manifest, there are three types of ports we are writing. It is essential to understand what each port is for. Nodeport is for external access, port is for what all services in cluster will talk using, target port is what service uses for load balancing.
- Once deployments and services are deployed, can use url generated by 'minikube service <service_name> --url' to access the same.
- Enter a pod using kubectl exec -it <podName> -- /bin/bash
- You can access other services from a container using curl <service_name>:<port number (5001 for eg)>
- Trying to get nginx to reverse proxy for all three flask apps with different location pathings didnt work. So, had to stick to just employee_service as reverse proxying. 
- If you get the kubectl handshake timeout/minikube no response: restart pc, start docker daemon, and start minikube.

***Prometheus & Grafana***

- Install helm, then add prometheus helm chart repo, deploy prom.
- Use get svc to check service name (mostly prometheus-server)
- Apply the prometheus config/changes using helm upgrade prometheus prometheus-community/prometheus -f values.yaml
- kubectl port-forward svc/prometheus-server 9090:80 + http://localhost:9090 (on local)
- Big bump in the road
    - Spent several hours trying to figure out why my flask-job in scrape metrics (prometheus server upgrade) wasn't showing as a target on the promUI. Could have left it when it wasn't working but kept digging and noticed that the changes to values.yaml were happening but configMap wasnt absorbing those changes, so had to manually edit it and delete pod to restart it and apply changes. 
    - This isn't sustianable as it wont detect future changes and this current manual change may get overwritten. Have figure out but moving ahead as the main purpose is accomplished. 
    - These kind of situations are a good test of what you are trying to derive from a project. I had learnt an okay amount about prom but I would have had that itch if I didnt get the job to display on the UI, so I persevered.
- Grafana:
    - Similar to prometheus, install grafana and using helm and kubectl, deploy it into the cluster. Do port forwarding to see it on your local.
    - Login with admin username and password generation instructions.
    - Configure prometheus as a data source and use the internal networking link http://prometheus-server.default.svc.cluster.local:80 as the link to prometheus.
    - open dashboards and create visualizations.
- If you clean up and delete all deployments/services, even the prom & grafana set up get deleted (I did this).

What is the difference exactly?
- Prometheus is meant to collect metrics and run queries. It doesn't focus on giving you the best UI. Prometheus has multiple pods for modularity each doing something else. Just list them out using kubectl.
- Grafana: It is just meant to be a good looking central point of all your metrics regardless of where it came from. So it isn't linked to just prometheus basically.

***Jenkins***

How this works is: jenkins is just pulling the code from the repo but is still running on the host at the end of the day. So, we need to have the docker daemon and minikube running on the host system (in my case, macOS).

- Install java and then jenkins. Then run the war file.
- Go to localhost:8080 and do the set up of login -> pipeline
- Create the jenkins file in the root directory of the repo and push to github
- Build the pipeline for the code which jenkins will fetch from github
- Jobs to be considered: build (build docker images), test (run container to run unittests), and deploy/delete (kubernetes). 
- The commands to be put in the Jenkinsfile is the same as what you would run if doing it locally, but this automtaes the process.
- Key hidden learning: env changes are lost after each sh '' ends, hence you need to do all the docker related commands under the same sh '' to make sure it has access to the minikube's docker env.
- sometimes even if you do rm container before rm image, it takes time to remove the container and then rm image will throw an error. Keep an eye out of that.

---


