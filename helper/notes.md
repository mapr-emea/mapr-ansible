## Create user and schema in Oracle

create user oozie identified by oozie;
GRANT CONNECT,RESOURCE,DBA TO oozie;


## Other notes for copying

export ANSIBLE_HOSTS=/Users/chufe/Documents/workspaces/mapr_ansible/hosts

wget -r -np -nH --cut-dirs=3 -R index.html http://archive.mapr.com/releases/v5.2.0/suse/
