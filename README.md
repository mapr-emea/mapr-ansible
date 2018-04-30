# MapR Ansible Scripts

This is a collection of Ansible scripts which help you to setup a MapR-cluster.

Maintainer: Carsten Hufe - Lead Data Engineer @ MapR

Changes, bugs and feature requests can be requested by using the Github issue tracker.
If you want to contribute to the project, open pull requests via Github.

The scripts support:

* Install MapR-Cluster including Ecosystem Components (only one playbook to execute)
* Modify an existing installation
    * Adding and removing components
    * Adding and decomissioning nodes
* The script also support dry-run on an installed cluster
* Aborted scripts can always re-run.
* Building Zeppelin
* Install MapR-Client
* Setting up Kerberos and generate Keytabs (only Redhat)
* Ansible modules to manage state of:
    * MapR volumes
    * MapR schedules
    * MapR Accountable Entities

## Supported MapR Versions

* MapR 6.0.1 with MEP 5.0.0 (branch master)
* MapR 6.0.0 with MEP 4.0.x (branch mapr-6.0.0-MEP-4.x)
* MapR 5.2.x (branch mapr-5.2-MEP-3.0.x)

## Supported OS

* Redhat 7 or higher
* CentOS 7 or higher
* Ubuntu 16.x
* Suse SLES 12 or higher

## Supported Security

* Unsecure mode
* MapR Native Security incl. Ecosystem Components
* Kerberos incl. Ecosystem Components

## Supported Databases

* Oracle (Hive, Hue and Oozie)
* MySQL (Hive, Hue and Oozie)
* Embedded databases

## Ansible

Ansible 2.4 or higher required!

If /usr/bin/python is not available link it (e.g. in Ubuntu 16.xx)

```
ansible -i myhosts/hosts_3nodes  -m raw -a "ln -s /usr/bin/python3 /usr/bin/python" all -v
```

## Verify inventory file

Execute:

```
ansible -i myhosts/<yourfile>  -m command -a "hostname -f" all
```

## Inventory file templates

Can be found `host_templates`

## Install cluster

Use `host_templates/hosts_cluster` as template and copy it and the hostnames to the components you want to get installed. If components are not required, just leave the block empty.
The configuration can be found in `group_vars/all`.

Then run:

```
ansible-playbook -i hosts_template site-cluster.yml
```

The `site-cluster.yml` script always ensures the cluster state. This means you can re-run this script, after you removed or added new components or nodes.
That an unprovisioned node is still known to Ansible you have to add the removed node to [unprovision] block in inventory file.

ATTENTION: Never move critical components in one run, e.g. you have two CLDB installed on node1 and node2 and you want move it to node3 and node4. In that case first install two new CLDBs and in
the next run remove the other ones.

## Install client

Use `host_templates/hosts_client` as template and copy it and the hostnames to the components you want to get installed. If components are not required, just leave the block empty. Then run:

```
ansible-playbook -i hosts_template site-client.yml
```

## Install RStudio Server (m5 license requried for NFS)

Ubuntu ONLY

Use `hosts_template` as template and copy it and the hostnames to the components you want to get installed. If components are not required, just leave the block empty. Then run:

```
ansible-playbook -i hosts_template sites/ext-rstudio-server.yml
```

## Install Zeppelin

Use `hosts_template` as template and copy it and the hostnames to the components you want to get installed. If components are not required, just leave the block empty. Then run:

```
ansible-playbook -i hosts_template sites/ext-zeppelin.yml
```

## Helpers

Helpers are located in the `helper` folder.

### Create several users to test ACE

This document contains the ACE file/Volume demo
To create the users and groups just run:

Run:

```
ansible-playbook -i hosts_template helper/create-user-ace.yml
```

### Setup Kerberos, SSSD and PAM with ActiveDirectory (Only tested on Redhat 7.3 and 7.4!!!)

Use `host_templates/hosts_kerberos` as template

```
ansible-playbook -i host_templates/hosts_kerberos sites/ext-kerberos-sssd-setup.yml
```

Afterwards authenticate with users from AD.

### Create Kerberos users in Active Directory for MapR

Based on number of hosts users are created in AD.

```
ansible-playbook -i host_templates/hosts_kerberos sites/ext-kerberos-createadusers.yml
```

### Generate keytabs based on created users in command above.

Keytabs are stored in folder defined in mapr_kerberos_local_keytabs_dir on ansible client machine

```
ansible-playbook -i host_templates/hosts_kerberos sites/ext-kerberos-keytabs-ad-generate.yml
```


### Verify keytabs which are the base for MapR installation

Keytabs are stored in folder defined in mapr_kerberos_local_keytabs_dir on ansible client machine.
When the customer delivers keytabs this can be also used to validate.

```
ansible-playbook -i host_templates/hosts_kerberos sites/ext-kerberos-keytabs-verify.yml
```

## Use Ansible modules for administrative tasks

### Volume management

The module always ensures the state. If a volume exists with these settings nothing will be changed.
The module also supports check mode!

```
- name: Create MapR volume
  mapr_volume:
    name: my.new.volume
    state: present
    topology: /data
    path: /test
    read_ace: p
    write_ace: p
    min_replication: 2
    replication: 3
    soft_quota_in_mb: 1024
    hard_quota_in_mb: 1024
    accountable_entity_type: user
    accountable_entity_name: mapr
    read_only: no
```

### Manage Schedules

The module always ensures the state. If a volume exists with these settings nothing will be changed.
The module also supports check mode!

```
- name: Modify MapR schedule
  mapr_schedule:
    name: testrule
    state: present
    rules:
      - frequency: daily
        time: 0
        retain: 7d
      - frequency: weekly
        date: sun
        time: 0
        retain: 4w
      - frequency: monthly
        date: "1"
        time: 0
        retain: 2m
```

### Manage Accountable Entities

The module always ensures the state. If a volume exists with these settings nothing will be changed.
The module also supports check mode!

```
- name: Modify MapR entity
  mapr_entity:
    name: mapr
    type: user
    email: abc@email.com
    soft_quota_in_mb: 1024
    hard_quota_in_mb: 1024
```

## Known issues

* When uprading, keys are not generated by ElasticSearch, but works with new installation (when upgrading set spyglass_elasticsearch_secure: false)
