#!/bin/bash
ansible-playbook -i inventory.txt check_flask_containers.yml
ansible-playbook -i inventory.txt nginx_installation.yml
tail -f /dev/null