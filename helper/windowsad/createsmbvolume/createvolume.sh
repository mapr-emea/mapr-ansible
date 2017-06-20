#!/bin/bash

YAMLFILE=$1
parse_yaml() {
    local prefix=$2
    local s
    local w
    local fs
    s='[[:space:]]*'
    w='[a-zA-Z0-9_]*'
    fs="$(echo @|tr @ '\034')"
    sed -ne "s|^\($s\)\($w\)$s:$s\"\(.*\)\"$s\$|\1$fs\2$fs\3|p" \
        -e "s|^\($s\)\($w\)$s[:-]$s\(.*\)$s\$|\1$fs\2$fs\3|p" "$1" |
    awk -F"$fs" '{
    indent = length($1)/2;
    vname[indent] = $2;
    for (i in vname) {if (i > indent) {delete vname[i]}}
        if (length($3) > 0) {
            vn=""; for (i=0; i<indent; i++) {vn=(vn)(vname[i])("_")}
            printf("%s%s%s=%s\\n", "'"$prefix"'",vn, $2, $3);
        }
    }'
}

PARSEDYAML=$(parse_yaml $YAMLFILE)
VOLUMENAME=$(echo -e $PARSEDYAML | grep "^volumename" | awk '{split($0,a,"="); print a[2]}')
READACE=$(echo -e $PARSEDYAML | grep "^readgroups" | awk '{split($0,a,"="); print a[2]}' | xargs -l -I {} getent group "{}" | awk -F  ":" '{ print "g:" $3 }' | paste -sd "|" -)
WRITEACE=$(echo -e $PARSEDYAML | grep "^writegroups" | awk '{split($0,a,"="); print a[2]}' | xargs -l -I {} getent group "{}" | awk -F  ":" '{ print "g:" $3 }' | paste -sd "|" -)
echo "Volume $VOLUMENAME"
echo "Read ACE=$READACE"
echo "Write ACE=$WRITEACE"
maprcli volume create -name $VOLUMENAME -type rw -readAce "$READACE" -writeAce "$WRITEACE" -path /shares/$VOLUMENAME
hadoop fs -chmod 777 /shares/$VOLUMENAME
hadoop fs -chown mapr:nobody /shares/$VOLUMENAME

