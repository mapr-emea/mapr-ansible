install
cdrom

lang en_US.UTF-8
keyboard us
timezone UTC

network --onboot yes --bootproto=dhcp --device=eth0 --activate --noipv6

rootpw vagrant
authconfig --enableshadow --passalgo=sha512
user --name=vagrant --groups=vagrant --password=vagrant

firewall --disabled
selinux --disabled
firstboot --disabled

bootloader --location=mbr
text
skipx

logging --level=info
zerombr
clearpart --all
ignoredisk --only-use=sda
autopart
#autopart --nolvm
services --enabled=ntpd,ntpdate,NetworkManager,sshd

reboot

%packages --nobase
@Core
openssh-clients
openssh-server
-iwl*firmware
%end
 
 
%post --log=/root/ks.log
 
echo "vagrant ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers.d/vagrant
echo "Defaults:vagrant !requiretty" >> /etc/sudoers.d/vagrant
chmod 0440 /etc/sudoers.d/vagrant

yum -y update
echo "End of Kickstart"
%end
