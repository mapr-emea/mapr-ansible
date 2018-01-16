#!/bin/bash

set -e

ansible-playbook -i myhosts/hosts_4nodes helper/fetch-mapr-keys.yml

input="myhosts/rollingnodes_order"
while IFS= read -r var
do
  ansible-playbook -i myhosts/hosts_3nodes site-upgrade.yml --limit $var -e rolling_upgrade=true
done < "$input"
ansible-playbook -i myhosts/hosts_3nodes helper/set-latest-version.yml
