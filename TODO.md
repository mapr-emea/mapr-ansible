Test
- switch from NFS to fuse
- Add node
- remove normal node
- add cldb node
- add zk node
- remove zk node
- add cldb node
- remote cldb node

demo.mapr.com secure=false ip-10-0-0-109.ps.mapr.com:7222 ip-10-0-0-15.ps.mapr.com:7222
demo.mapr.com secure=true ip-10-0-0-38.ps.mapr.com:7222
my.cluster.com secure=false kerberosEnable=true cldbPrincipal=princiop localhost:7222


ip-10-0-0-152 ~]# maprcli service list
logpath                                                            displayname         name                 state  
/opt/mapr/httpfs/httpfs-1.0/logs                                   Httpfs              httpfs               0      
/opt/mapr/hive/hive-2.1/logs/mapr                                  HiveServer2         hs2                  0      
/opt/mapr/spark/spark-2.1.0/logs/                                  SparkHistoryServer  spark-historyserver  0      
/opt/mapr/oozie/oozie-4.3.0/logs                                   Oozie               oozie                0      
/opt/mapr/logs/cldb.log                                            CLDB                cldb                 0      
/opt/mapr/logs/hoststats.log                                       HostStats           hoststats            0      
/opt/mapr/collectd/collectd-5.7.1/var/log/collectd                 CollectD            collectd             0      
/opt/mapr/fluentd/fluentd-0.14.00/var/log/fluentd/fluentd.log      Fluentd             fluentd              0      
/opt/mapr/hue-livy/hue-livy-3.12.0/logs/                           HueLivyServer       livy                 0      
/opt/mapr/hive/hive-2.1/logs/mapr                                  HiveMetastore       hivemeta             0      
/opt/mapr/logs/mfs.log                                             FileServer          fileserver           0      
/opt/mapr/elasticsearch/elasticsearch-2.3.3/var/log/elasticsearch  ES                  elasticsearch        0      
/opt/mapr/grafana/grafana-4.1.2/var/log/grafana                    Grafana             grafana              0      
/opt/mapr/hadoop/hadoop-2.7.0/logs                                 ResourceManager     resourcemanager      0      
/opt/mapr/hadoop/hadoop-2.7.0/logs                                 JobHistoryServer    historyserver        0      
/opt/mapr/hue/hue-3.12.0/logs/                                     HueWebServer        hue                  0      
/opt/mapr/hadoop/hadoop-2.7.0/logs                                 NodeManager         nodemanager          0      
/opt/mapr/logs/adminuiapp.log                                      Webserver           webserver            0      
/opt/mapr/kibana/kibana-4.5.4/var/log/kibana                       Kibana              kibana               0      
/opt/mapr/opentsdb/opentsdb-2.3.0/var/log/opentsdb                 OpenTsdb            opentsdb             0      
/opt/mapr/logs/gateway.log                                         GatewayService      gateway              0   
ste correct owner /opt/mapr/kibana/kibana-4.5.4/config/key.pem

- Uninstall removed components from inventory
- Make installable for local install
- Add precheck for disks
- add sdparm lsbcore...
- read versions from FS not from config.

- RStudio for Redhat, Centos, Suse
- Add storm
- Add warden restart handler http://stackoverflow.com/questions/22649333/ansible-notify-handlers-in-another-role

http://maprdocs.mapr.com/home/AdvancedInstallation/InstallMonitoring.html

/opt/mapr/server/configure.sh -C ip-10-0-0-10.eu-west-1.compute.internal,ip-10-0-0-8.eu-west-1.compute.internal,ip-10-0-0-9.eu-west-1.compute.internal -Z ip-10-0-0-10.eu-west-1.compute.internal,ip-10-0-0-8.eu-west-1.compute.internal,ip-10-0-0-9.eu-west-1.compute.internal  -N my.cluster.com -RM framework2.marathon.mesos  -HS jobhistory.framework2.mesos -MF framework2  -MCL framework2

/opt/mapr/server/configure.sh -N ip-10-0-0-166.eu-west-1.compute.internal -Z ip-10-0-0-166.eu-west-1.compute.internal -C ip-10-0-0-166.eu-west-1.compute.internal -u mapr -g mapr -secure -RM ip-10-0-0-166.eu-west-1.compute.internal -HS ip-10-0-0-166.eu-west-1.compute.internal

https://www.rstudio.com/products/rstudio/download-commercial/

https://community.mapr.com/community/exchange/content?filterID=contentstatus%5Bpublished%5D~category%5Bspyglass-dashboards%5D



