import os,json,re

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_mapr_installed_packages(host):
    for p in [
        "mapr-zookeeper",
        "mapr-cldb",
        "mapr-fileserver",
        "mapr-resourcemanager",
        "mapr-historyserver",
        "mapr-nodemanager",
        "mapr-core",
        "mapr-core-internal",
        "mapr-mapreduce2",
        "mapr-zk-internal",
        "mapr-spark",
        "mapr-oozie",
        "mapr-librdkafka",
        "mapr-hadoop-core",
        "mapr-spark-historyserver",
        "mapr-oozie-internal"
    ]:
        assert host.package(p).is_installed


def test_mapr_not_installed_packages(host):
    for p in [
        "mapr-nfs",
        "mapr-gateway",
        "mapr-posix-client-basic",
        "mapr-posix-client-platinum"
    ]:
        assert not host.package(p).is_installed


def test_mapr_configfiles(host):
    for f in [
        "maprserverticket",
        "cldb.key",
        ".customSecure",
        "ssl_keystore",
        "ssl_truststore",
        "ssl_truststore.pem"
    ]:
        assert host.file("/opt/mapr/conf/" + f).exists

def test_mapr_hadoop_configfiles(host):
    source_folder = "/opt/mapr/hadoop/hadoop-2.7.0/etc/hadoop/"
    for f in [
            "core-site.xml",
            "yarn-site.xml"
            ]:
        assert host.file(source_folder + f).exists

def test_service_started(host):
    assert host.service("mapr-zookeeper").is_running
    assert host.service("mapr-warden").is_running


def test_yarn_config_with_kerberos(host):
    vars = host.ansible.get_variables()
    f = host.file("/opt/mapr/hadoop/hadoop-2.7.0/etc/hadoop/yarn-site.xml")
    assert f.exists
    assert """<property>
    <name>yarn.resourcemanager.ha.custom-ha-enabled</name>
    <value>true</value>
    <description>MapR Zookeeper based RM Reconnect Enabled. If this is true, set the failover proxy to be the class MapRZKBasedRMFailoverProxyProvider</description>
  </property>
  <property>
    <name>yarn.client.failover-proxy-provider</name>
    <value>org.apache.hadoop.yarn.client.MapRZKBasedRMFailoverProxyProvider</value>
    <description>Zookeeper based reconnect proxy provider. Should be set if and only if mapr-ha-enabled property is true.</description>
  </property>
  <property>
    <name>yarn.resourcemanager.recovery.enabled</name>
    <value>true</value>
    <description>RM Recovery Enabled</description>
  </property>
  <property>
   <name>yarn.resourcemanager.ha.custom-ha-rmaddressfinder</name>
   <value>org.apache.hadoop.yarn.client.MapRZKBasedRMAddressFinder</value>
  </property>

  <property>
    <name>yarn.acl.enable</name>
    <value>true</value>
  </property>
  

  <!-- :::CAUTION::: DO NOT EDIT ANYTHING ON OR ABOVE THIS LINE -->
    <!-- fix for Oozie when user different than mapr -->
    <property>
        <name>yarn.resourcemanager.principal</name>
        <value>mapr</value>
    </property>
    <property>
        <name>yarn.nodemanager.container-executor.class</name>
        <value>org.apache.hadoop.yarn.server.nodemanager.LinuxContainerExecutor</value>
    </property>
    <property>
        <name>yarn.nodemanager.linux-container-executor.group</name>
        <value>mapr</value>
    </property>
    <property>
        <name>yarn.log-aggregation-enable</name>
        <value>false</value>
    </property>
    <property>
        <name>yarn.scheduler.maximum-allocation-mb</name>
        <value>131072</value>
        <description>The maximum allocation for every container request at the RM, in MBs. Memory requests higher than this will throw a InvalidResourceRequestException.</description>
    </property>
    <property>
        <name>yarn.resourcemanager.am.max-attempts</name>
        <value>4</value>
        <description>The maximum number of application attempts</description>
    </property>""" in f.content

def test_hadoop_fs(host):
    cmd = host.run("echo mapr | maprlogin password -user mapr")
    assert "MapR credentials of user 'mapr' for cluster 'molecule-cluster' are written to" in cmd.stdout
    cmd = host.run("hadoop fs -ls -d /user/mapr")
    cmd_dir_pattern = re.compile(ur'(drwx.*mapr mapr.*/user/mapr)')
    assert re.findall(cmd_dir_pattern, cmd.stdout)

def helper_test_yarn_application(host):
    apps = host.run("curl -u mapr:mapr --cacert /opt/mapr/conf/ssl_truststore.pem -X GET -H \"Content-Type:application/json\" https://basic-core:8090/ws/v1/cluster/apps")
    state = sorted(json.loads(apps.stdout)['apps']['app'], key=lambda k: k['startedTime'], reverse=True)[0]['finalStatus']
    assert state == "SUCCEEDED"

def test_yarn(host):
    host.run("/opt/mapr/hadoop/hadoop-2.7.0/bin/yarn jar /opt/mapr/hadoop/hadoop-2.7.0/share/hadoop/mapreduce/hadoop-mapreduce-examples-2.7.0-mapr-1808.jar pi 5 10")
    helper_test_yarn_application(host)

def test_hadoop(host):
    host.run("hadoop jar /opt/mapr/hadoop/hadoop-2.7.0/share/hadoop/mapreduce/hadoop-mapreduce-examples-2.7.0-mapr-1808.jar pi 5 10")
    helper_test_yarn_application(host)
