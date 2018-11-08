#!/bin/bash

CERT_PATH=~/testsslkeys
CLUSTER_NAME=demo.mapr.com
RESULT=$(ansible -i myhosts/hosts_3nodes -m shell -a 'echo "|host=$(hostname --ip-address)"' all)

for i in $(echo $RESULT | tr "|" "\n")
do
    if [[ "$i" =~ ^host ]]
    then
        export NODEIP=$(echo $i | cut -d "=" -f2-)
        export NODENUMBER=$(echo $NODEIP | cut -d "." -f4-)
        export NODENAME=ip-10-0-0-${NODENUMBER}.ps.mapr.com
        cat helper/ssl/cert_tpl | envsubst > $CERT_PATH/$NODENAME.conf
        openssl req -nodes -newkey rsa:4096 -keyout $CERT_PATH/key/$NODENAME.pem -out $CERT_PATH/$NODENAME.csr -config $CERT_PATH/$NODENAME.conf
        openssl x509 -req -in $CERT_PATH/$NODENAME.csr -CA $CERT_PATH/rootCA.pem -CAkey $CERT_PATH/rootCA-private.key -CAcreateserial -out $CERT_PATH/crt/$NODENAME.pem -days 1024 -sha256
    fi
done
