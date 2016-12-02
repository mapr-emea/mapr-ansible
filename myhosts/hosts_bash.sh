#!/bin/bash

NODE1=10.0.0.19
NODE2=10.0.0.20
NODE3=10.0.0.21

cat << EOF
{
    "base"   : {
        "hosts"   : [ "$NODE1","$NODE2","$NODE3"],
        "vars" : {
            "ansible_user" :  "centos",
            "ansible_become" :  "yes",
            "ansible_become_method" :  "sudo"
        }
    },
    "mapr-core" : {
        "hosts"   : [ "$NODE1",
                      "$NODE2",
                      "$NODE3"
                    ],
         "vars" : {
             "ansible_user" :  "centos",
             "ansible_become" :  "yes",
             "ansible_become_method" :  "sudo"
         }
    },
    "mapr-zookeeper" : {
        "hosts"   : [ "$NODE1",
                      "$NODE2",
                      "$NODE3"
                    ],
         "vars" : {
             "ansible_user" :  "centos",
             "ansible_become" :  "yes",
             "ansible_become_method" :  "sudo"
         }
    },
    "mapr-cldb" : {
        "hosts"   : [ "$NODE1",
                      "$NODE2",
                      "$NODE3"
                    ],
        "vars" : {
            "ansible_user" :  "centos",
            "ansible_become" :  "yes",
            "ansible_become_method" :  "sudo"
        }
    },
    "mapr-gateway" : {
        "hosts"   : ["$NODE1"],
        "vars" : {
            "ansible_user" :  "centos",
            "ansible_become" :  "yes",
            "ansible_become_method" :  "sudo"
        }
    },
     "mapr-mcs" : {
         "hosts"   : ["$NODE1"],
        "vars" : {
            "ansible_user" :  "centos",
            "ansible_become" :  "yes",
            "ansible_become_method" :  "sudo"
        }
     },
     "mapr-resourcemanager" : {
         "hosts"   : [ "$NODE1",
                       "$NODE2"
                     ],
        "vars" : {
            "ansible_user" :  "centos",
            "ansible_become" :  "yes",
            "ansible_become_method" :  "sudo"
        }
     },
     "mapr-historyserver" : {
         "hosts"   : ["$NODE1"],
        "vars" : {
            "ansible_user" :  "centos",
            "ansible_become" :  "yes",
            "ansible_become_method" :  "sudo"
        }
     },
    "mapr-datanode" : {
        "hosts"   : [ "$NODE1",
                      "$NODE2",
                      "$NODE3"
                    ],
        "vars" : {
            "ansible_user" :  "centos",
            "ansible_become" :  "yes",
            "ansible_become_method" :  "sudo"
        }
    },
     "mapr-spark-yarn" : {
         "hosts"   : ["$NODE1"],
         "vars" : {
             "ansible_user" :  "centos",
             "ansible_become" :  "yes",
             "ansible_become_method" :  "sudo"
         }
     },
     "mapr-spark-historyserver" : {
         "hosts"   : ["$NODE1"],
        "vars" : {
            "ansible_user" :  "centos",
            "ansible_become" :  "yes",
            "ansible_become_method" :  "sudo"
        }
     },
     "mapr-nfs"     : {
         "children": [ "base" ]
     },
     "mapr-drill"     : {
         "children": [ "base" ]
     },
     "mapr-hbase-cli"     : {
         "children": [ "base" ]
     }
}
EOF
