export SPARK_HOME={{ spark_path_result.files[0].path }}
export HADOOP_HOME=/opt/mapr/hadoop/hadoop-{{ hadoop_version }}
export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop