#!/bin/bash

set -e

ansible-playbook -i myhosts/hosts_5nodes helper/fetch-mapr-keys.yml

input="myhosts/rollingnodes"
while IFS= read -r var
do
  ansible-playbook -i myhosts/hosts_5nodes site-upgrade.yml --limit $var
done < "$input"