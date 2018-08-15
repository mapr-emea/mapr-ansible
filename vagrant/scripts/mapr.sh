#!/bin/bash

cd ~
git clone https://github.com/mapr-emea/mapr-ansible.git
cd mapr-ansible
git checkout vagrant
ansible-playbook -i vagrant/ansible_inventory/hosts_mapr_slim site-cluster.yml

maprcli volume list -json | jq '.data[].volumename' | xargs -L 1 maprcli volume modify -replication 1 -minreplication 1 -name
maprcli volume list -json | jq '.data[].volumename' | xargs -L 1 maprcli volume modify -nsreplication 1 -nsminreplication 1 -name
maprcli alarm clearall
