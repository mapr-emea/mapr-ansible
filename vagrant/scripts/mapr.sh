#!/bin/bash

echo "echo ''" >> /home/vagrant/.bashrc
echo "echo 'Welcome to MapR Vagrant Sandbox'" >> /home/vagrant/.bashrc
echo "echo 'Switch to mapr-user: sudo su - mapr'" >> /home/vagrant/.bashrc
echo "echo 'Create a mapr-user ticket: maprlogin password'" >> /home/vagrant/.bashrc
echo "echo '... enter password mapr'" >> /home/vagrant/.bashrc
echo "echo ''" >> /home/vagrant/.bashrc

cd ~
git clone https://github.com/mapr-emea/mapr-ansible.git
cd mapr-ansible
git checkout vagrant
ansible-playbook -i vagrant/$MAPR_ANSIBLE_INVENTORY --extra-vars "$MAPR_ANSIBLE_EXTRA_VARS" site-cluster.yml
cd ~
rm -Rf mapr-ansible

maprcli volume list -json | jq '.data[].volumename' | xargs -L 1 maprcli volume modify -replication 1 -minreplication 1 -name
maprcli volume list -json | jq '.data[].volumename' | xargs -L 1 maprcli volume modify -nsreplication 1 -nsminreplication 1 -name
maprcli alarm clearall

systemctl stop mapr-posix-client-basic | true
systemctl stop mapr-warden
systemctl stop mapr-zookeeper
