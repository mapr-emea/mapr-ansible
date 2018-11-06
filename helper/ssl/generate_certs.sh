#/bin/bash

CERT_PATH=~/testsslkeys
CLUSTER_NAME=demo.mapr.com

RESULT=$(ansible -i myhosts/hosts_3nodes -m shell -a 'echo "|host=$(hostname -f)"' all)

for i in $(echo $RESULT | tr "|" "\n")
do
    if [[ "$i" =~ ^host ]]
    then
        NODENAME=$(echo $i | cut -d "=" -f2-)
        openssl genrsa -out $CERT_PATH/$NODENAME.key 4096
        openssl req -new -key $CERT_PATH/$NODENAME.key -out $CERT_PATH/$NODENAME.csr -subj "/C=DE/O=MapR/OU=MapR PS/CN=$NODENAME"
        openssl x509 -req -in $CERT_PATH/$NODENAME.csr -CA $CERT_PATH/rootCA.pem -CAkey $CERT_PATH/rootCA-private.key -CAcreateserial -out $CERT_PATH/$NODENAME.crt -days 1024 -sha256
   #     rm -f $CERT_PATH/$NODENAME.p12
   #     openssl pkcs12 -export -in $CERT_PATH/$NODENAME.crt -inkey $CERT_PATH/$NODENAME.key -out $CERT_PATH/$NODENAME.p12 -name $CLUSTER_NAME -password pass:mapr123
    fi
done
