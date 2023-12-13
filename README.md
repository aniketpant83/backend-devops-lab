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

---

**Steps to run code**

- Clone repo to a directory and open on VSCode or editor of choice.
- Install Docker (and if needed, other things too) and run 'docker compose up' from project root directory
- This will run the 3 microservices, unit tests for all 3, and ansible playbooks.
- Use to ctrl+c to stop the containers and then docker-compose down to delete containers. Remember to delete images for cleanup
- Expected result of unit tests should be 17 tests running and passing, and ansible playbook with 8 oks and 7 changed, 0 fails.

---

**Learnings:**

- Docker:
    - The KEY difference in trying to make different services interact with each other, that wasnt caught in the react to flask communictaion from previous project, is that js loads onto browser and can fetch 'localhost' requests. However, in this project, containers cant talk to each other.


- Ansible:
    Learnt the most here. Documented the files to explain in the places itself. However, will list what I learnt as I did. Refer to the ansible files to read along with the below points.
    1. inventory.txt: creating a group called local in inventory and then putting localhost with ansible_connection=local will work when testing but we need to change that to docker as we test the same out in containers.
    2. nginx.conf.j2: dont forget to put http:// before <container_name:port_name>.
    3. run_playbook.sh: running two playbooks and cant put both in CMD stanza in the dockerfile, so created a shell script and added both. Also added script to stop container from shutting after execution of playbook so I can leave it open for debugging.
    4. playbooks are quite self-explanatory. Was running into an issue with nginx reverse proxy, but I think it was because I hadnt written the script to start it before I was trying to reload it. Also, service module caused failure, so had to swtich to command module to run it, and that worked.
    5. Dockerfile: The step to install sudo is there because Ansible was failing at the become module. Maybe some issues with docker not having sudo baked in which ansible needs.  

---

WIP: 
Kubernetes, Jenkins