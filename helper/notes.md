http://maprdocs.mapr.com/home/Hue/ConfigureHueOracleDB.html
CentOS	yum install gcc python-devel
SuSE	zypper install gcc python-devel
Ubuntu	apt-get install gcc python-dev
Configure these parameters related to ORACLE_HOME:
Ensure that there is an ORACLE_HOME variable in your environment and that this variable contains the path to the directory for the Oracle installation:
export ORACLE_HOME=<path_to_oracle>
Ensure that libraries in ORACLE_HOME are available to the library folder:
export LD_LIBRARY_PATH="$ORACLE_HOME:$LD_LIBRARY_PATH"
Ensure that there is a libclntsh.so library inside ORACLE_HOME:
cd $ORACLE_HOME
ln -s libclntsh.so.11.* libclntsh.so


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
