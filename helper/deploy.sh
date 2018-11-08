#!/bin/bash

SCRIPT=$(readlink -f $0)
SCRIPTPATH=`dirname $SCRIPT`
cd $SCRIPTPATH
CURRENT_GIT_REVISION=$(git rev-parse HEAD | tr -d '[:space:]')
APPROVED_GIT_REVISION=$(grep "git_revision_approved=" $1 | cut -d "=" -f2- | tr -d '[:space:]')
CURRENT_GIT_BRANCH=$(git branch | grep \* | cut -d ' ' -f2)
GIT_UNCOMMITTED_CHANGES=`[ $(git status | grep "nothing to commit") ] && echo "no" || echo "yes"`
CLUSTER_NAME=$(grep "cluster_name=" $1 | cut -d "=" -f2- | tr -d '[:space:]')

echo "======================================="
echo "Cluster to deploy: $CLUSTER_NAME"
echo "Current Git revision: $CURRENT_GIT_REVISION"
echo "Approved Git revision: $APPROVED_GIT_REVISION"
echo "Git branch: $CURRENT_GIT_BRANCH"
echo "Git uncommitted changes: $GIT_UNCOMMITTED_CHANGES"

if [[ "$CURRENT_GIT_REVISION" != "$APPROVED_GIT_REVISION" && "$CLUSTER_NAME" != "lab.cluster.com" ]]
then
    echo ""
    echo "... deployment aborted, since the approved and current Git revisions are different."
    exit 1
fi

echo "Continue? (yes/no)"
read CONTINUE
if [[ "$CONTINUE" != "yes" ]]
then
    echo ""
    echo "... deployment aborted."
    exit 1
fi

echo "... continuing."
export LOG_DATE=`date '+%Y-%m-%d-%H-%M-%S'`
echo $LOG_DATE
export ANSIBLE_LOG_PATH="/var/log/mapr-ansible.${CLUSTER_NAME}.${LOG_DATE}.log"
echo "... logging Ansible log to $ANSIBLE_LOG_PATH"
ansible-playbook --vault-id @prompt -i $1 site-cluster.yml
