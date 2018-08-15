#!/bin/bash

echo "debug: Executing scripts/base.sh"
hostname -F /etc/hostname
hostname maprdemo
echo "maprdemo" > /etc/hostname

cat <<EOF > /etc/hosts
127.0.0.1 maprdemo localhost.localdomain localhost loopback
EOF


yum install -y deltarpm epel-release

yum -y update
yum -y install gcc make gcc-c++ kernel-devel kernel-headers perl wget bzip2 tree git jq pv ansible
yum clean all

sed -i 's/.*UseDNS.*/UseDNS no/' /etc/ssh/sshd_config

# set timezone UTC0
timedatectl set-timezone UTC
# Don't read the RTC time in the local time zone
timedatectl set-local-rtc 0

echo "Restarting VM"
shutdown -r now
