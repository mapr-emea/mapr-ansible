#!/bin/bash -x

echo "debug: Executing scripts/virtualbox.sh"

mount -o loop /home/vagrant/VBoxGuestAdditions.iso /mnt
sh /mnt/VBoxLinuxAdditions.run
rc=$?

umount /mnt
rm -rf /home/vagrant/VBoxGuestAdditions.iso

if [ $rc -ne 0 ]
then
    cat /var/log/VBoxGuestAdditions.log
    exit $rc
else
    echo "Virtualbox guest addons have been installed successfully"
    exit 0
fi