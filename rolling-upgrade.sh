#!/bin/bash

set -e

# TODO fetch cldb config files. is not executed

input="myhosts/rollingnodes"
while IFS= read -r var
do
  ansible-playbook -i myhosts/hosts_5nodes site-upgrade.yml --limit $var
done < "$input"