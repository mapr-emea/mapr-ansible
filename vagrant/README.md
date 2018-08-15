# How to build and run

## Requirements

Building the images for VirtualBox requires

* VirtualBox
* Vagrant
* Packer

## MapR 6.0.1 with MEP 5.0 (Spark)

```
packer build -var-file vars/mapr-6.0.1_MEP-5.0.0-slim.json vagrant-mapr-centos-local.json
vagrant box add --force 'devproof/mapr-6.0.1_MEP-5.0.0-slim' mapr-6.0.1_MEP-5.0.0-slim.box
cd vagrantfiles/mapr-6.0.1_MEP-5.0.0-slim
vagrant up
```

## MapR 6.0.1 with MEP 5.0 (Spark, Hive)

```
packer build -var-file vars/mapr-6.0.1_MEP-5.0.0-hive.json vagrant-mapr-centos-local.json
vagrant box add --force 'devproof/mapr-6.0.1_MEP-5.0.0-hive' mapr-6.0.1_MEP-5.0.0-hive.box
cd vagrantfiles/mapr-6.0.1_MEP-5.0.0-hive
vagrant up
```

## MapR 6.0.1 with MEP 5.0 (Spark, Hive, Drill)

```
packer build -var-file vars/mapr-6.0.1_MEP-5.0.0-hive-drill.json vagrant-mapr-centos-local.json
vagrant box add --force 'devproof/mapr-6.0.1_MEP-5.0.0-hive-drill' mapr-6.0.1_MEP-5.0.0-hive-drill.box
cd vagrantfiles/mapr-6.0.1_MEP-5.0.0-hive-drill
vagrant up
```
