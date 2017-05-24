[[database]]
    engine=oracle
    host=node1
    port=1521
    user=hue
    password=hue_password
    name=MAPR
    options={'threaded':true}

cd /opt/mapr/hue/hue-<version>
source ./build/env/bin/activate
pip install cx_Oracle (geht auch mit pfad)
hue syncdb --noinput
hue migrate
deactivate

## Create user and schema in Oracle
DROP USER oozie CASCADE;
CREATE USER oozie IDENTIFIED BY oozie;
GRANT ALL PRIVILEGES TO oozie;
GRANT CONNECT, RESOURCE TO oozie;
DROP USER hue CASCADE;
CREATE USER hue IDENTIFIED BY hue;
GRANT ALL PRIVILEGES TO hue;
GRANT CONNECT, RESOURCE TO hue;
DROP USER hive CASCADE;
CREATE USER hive IDENTIFIED BY hive;
GRANT ALL PRIVILEGES TO hive;
GRANT CONNECT, RESOURCE TO hive;



CREATE USER oozie IDENTIFIED BY oozie;
GRANT ALL PRIVILEGES TO oozie;
GRANT CONNECT, RESOURCE TO oozie;
QUIT;

CREATE USER hue IDENTIFIED BY hue;
GRANT ALL PRIVILEGES TO hue;
GRANT CONNECT, RESOURCE TO hue;
QUIT;

CREATE USER hive IDENTIFIED BY hive;
GRANT ALL PRIVILEGES TO hive;
GRANT CONNECT, RESOURCE TO hive;
QUIT;


create user oozie identified by oozie;
GRANT CONNECT,RESOURCE,DBA TO oozie;

## Other notes for copying

export ANSIBLE_HOSTS=/Users/chufe/Documents/workspaces/mapr_ansible/hosts

wget -r -np -nH --cut-dirs=3 -R index.html http://archive.mapr.com/releases/v5.2.0/suse/
