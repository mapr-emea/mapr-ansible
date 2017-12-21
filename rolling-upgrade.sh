#!/bin/bash

set -e

ansible-playbook -i myhosts/hosts_4nodes helper/fetch-mapr-keys.yml

input="myhosts/rollingnodes"
while IFS= read -r var
do
  ansible-playbook -i myhosts/hosts_4nodes site-upgrade.yml --limit $var -e rolling_upgrade=true
done < "$input"
ansible-playbook -i myhosts/hosts_kerberos2 helper/set-latest-version.yml
