
test security
use spark security from other project -> change to full template
test dry run

--> Create custom secure: https://maprdocs.mapr.com/home/SecurityGuide/Custom-security-in-mapr.html
add mapr-filemigrate
add mapr-spark-thriftserver-2.1.0.201711121518-1.noarch.rpm
add mapr-tez

-> in MCS fehlt CPU stats
Elastic search broken?


https://maprdocs.mapr.com/home/AdvancedInstallation/InstallMonitoring.html
for secure cluster monitoring:
/opt/mapr/server/configure.sh -OT <comma-separated list of OpenTSDB nodes> -ES <comma-separated list of Elasticsearch nodes> -R -EPelasticsearch -genESKeys