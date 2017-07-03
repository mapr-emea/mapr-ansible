#!/bin/bash

MAPR_HOME=${MAPR_HOME:-/opt/mapr}
CLUSTERNAME=${CLUSTERNAME:-mycluster}
export MAPR_TICKETFILE_LOCATION=/opt/mapr/conf/mapruserticket

#
# Create and apply MapR license file
#
configureMapRLicense()
{
    #
    # Locate or generate the cluster ID
    #
    echo "Fetching cluster ID..."
    if [ ! -f "$MAPR_HOME/conf/clusterid" ]; then
       echo "File clusterid not found, creating file..."
       maprcli license showid | tail -1 > $MAPR_HOME/conf/clusterid
    fi

    CLUSTERID=$(cat $MAPR_HOME/conf/clusterid)
    echo "Cluster ID: $CLUSTERID"

    #
    # Request a JSON license file
    #
    echo "Fetching JSON license ..."
    RESULTS=$(wget -O /tmp/${CLUSTERID}.json "https://mapr-installer-dialhome.appspot.com/lic?license_type=m5trial&user_id=55143&cluster_id=$CLUSTERID&cluster_name=$CLUSTERNAME" 2>&1)
    STATUS=$?

    if [ $STATUS -ne 0 ]; then
        echo " "
        echo "wget failed: $RESULTS"
        echo " "
        exit 1
    fi

    echo "Saved JSON license file to: /tmp/${CLUSTERID}.json"

    #
    # Convert the JSON file to a text file
    #
 echo "Converting JSON format to text..."
    cat /tmp/${CLUSTERID}.json | sed -e 's|\\r||g' \
                                     -e 's|\\"|"|g' \
                                     -e 's|\\n|\n|g' \
                                     -e 's|^.*-----BEGIN SIGNED|-----BEGIN SIGNED|' \
                                     -e 's|-----END SIGNATURE-----.*|-----END SIGNATURE-----\n|g' > /tmp/${CLUSTERID}.lic
    echo "Saved license file to: /tmp/${CLUSTERID}.lic"

    echo "Adding M5 trial license to cluster..."
    RESULTS=$(maprcli license add -license /tmp/${CLUSTERID}.lic -is_file true 2>&1)

    STATUS=$?
    if [ $STATUS -ne 0 ]; then
        echo " "
        echo "         Unable to add /tmp/${CLUSTERID}.lic: $RESULTS"
        echo " "
        exit 1
    fi

    echo "License successfully added!"
}


configureMapRLicense
exit 0

