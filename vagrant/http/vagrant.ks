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
clearpart --all --initlabel
autopart
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

#mkdir -pm 700 /home/vagrant/.ssh
#curl -o /home/vagrant/.ssh/authorized_keys https://raw.githubusercontent.com/mitchellh/vagrant/master/keys/vagrant.pub
#cat <<EOK >/home/vagrant/.ssh/authorized_keys
#ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA6NF8iallvQVp22WDkTkyrtvp9eWW6A8Y\
#Vr+kz4TjGYe7gHzIw+niNltGEFHzD8+v1I2YJ6oXevct1YeS0o9HZyN1Q9qgCgzUFtdO\
#KLv6IedplqoPkcmF0aYet2PkEDo3MlTBckFXPITAMzF8dJSIFo9D8HfdOV0IAdx4O7Pt\
#ixWKn5y2hMNG0zQPyUecp4pzC6kivAIhyfHilFR61RGL+GPXQ2MWZWFYbAGjyiYJnAmC\
#P3NOTd0jMZEnDkbUvxhMmBYSdETk1rRgm+R4LOzFUGaHqHDLKLX+FIPKcF96hrucXzcW\
#yLbIbEgE98OHlnVYCzRdK8jlqm8tehUc9c9WhQ== vagrant insecure public key
#EOK
#chmod 0600 /home/vagrant/.ssh/authorized_keys
#chown -R vagrant:vagrant /home/vagrant/.ssh
yum -y update
echo "End of Kickstart"
%end
