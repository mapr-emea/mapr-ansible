- Uninstall removed components from inventory
- Make installable for local install
- Add precheck for disks

- RStudio for Redhat, Centos, Suse
- Add storm
- Add warden restart handler http://stackoverflow.com/questions/22649333/ansible-notify-handlers-in-another-role

http://maprdocs.mapr.com/home/AdvancedInstallation/InstallMonitoring.html

/opt/mapr/server/configure.sh -C ip-10-0-0-10.eu-west-1.compute.internal,ip-10-0-0-8.eu-west-1.compute.internal,ip-10-0-0-9.eu-west-1.compute.internal -Z ip-10-0-0-10.eu-west-1.compute.internal,ip-10-0-0-8.eu-west-1.compute.internal,ip-10-0-0-9.eu-west-1.compute.internal  -N my.cluster.com -RM framework2.marathon.mesos  -HS jobhistory.framework2.mesos -MF framework2  -MCL framework2

/opt/mapr/server/configure.sh -N ip-10-0-0-166.eu-west-1.compute.internal -Z ip-10-0-0-166.eu-west-1.compute.internal -C ip-10-0-0-166.eu-west-1.compute.internal -u mapr -g mapr -secure -RM ip-10-0-0-166.eu-west-1.compute.internal -HS ip-10-0-0-166.eu-west-1.compute.internal

https://www.rstudio.com/products/rstudio/download-commercial/

https://community.mapr.com/community/exchange/content?filterID=contentstatus%5Bpublished%5D~category%5Bspyglass-dashboards%5D



## Other notes for copying

export ANSIBLE_HOSTS=/Users/chufe/Documents/workspaces/mapr_ansible/hosts

wget -r -np -nH --cut-dirs=3 -R index.html http://archive.mapr.com/releases/v5.2.0/suse/
