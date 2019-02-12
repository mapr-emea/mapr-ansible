export METASTORE_PORT=9083
{% if hive_with_tez %}
export TEZ_CONF_DIR={{ tez_path_result.files[0].path }}/conf
export TEZ_JARS={{ tez_path_result.files[0].path }}/*:{{ tez_path_result.files[0].path }}/lib/*
export HADOOP_CLASSPATH=$TEZ_CONF_DIR:$TEZ_JARS:$HADOOP_CLASSPATH
{% endif %}
{% if hive_server_security == 'pam' %}
export HADOOP_OPTS="-Dmapr_sec_enabled=true $HADOOP_OPTS"
{% endif %}