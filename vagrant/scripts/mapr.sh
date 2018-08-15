#!/bin/bash

cd ~
git clone https://github.com/mapr-emea/mapr-ansible.git
cd mapr-ansible
git checkout vagrant
ansible-playbook -i vagrant/ansible_inventory/hosts_mapr_slim site-cluster.yml --extra-vars "disks=/dev/sdb disk_storage_pool_size=1"
cd ~
rm -Rf mapr-ansible

export MAPR_TICKETFILE_LOCATION=/opt/mapr/conf/mapruserticket

maprcli volume list -json | jq '.data[].volumename' | xargs -L 1 maprcli volume modify -replication 1 -minreplication 1 -name
maprcli volume list -json | jq '.data[].volumename' | xargs -L 1 maprcli volume modify -nsreplication 1 -nsminreplication 1 -name
maprcli alarm clearall
