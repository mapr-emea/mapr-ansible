#!/bin/python

import subprocess
import json
import socket


class VolumeDataDistribution(object):
    def __init__(self, volumename):
        self.volumename = volumename
        self.affectedRacks = set()
        self.outOfTopologyContainerIdsContainers = []
        self.outOfTopologyContainerIdsReplicas = []
        self.topologyContainerIdsRacks1 = []
        self.topologyContainerIdsRacks2 = []
        self.topologyContainerIdsRacks3 = []
        self.topologyContainerIdsRacks4 = []
        self.topologyContainerIdsRacks5 = []
        self.topologyContainerIdsRacks6 = []
        self.topologyContainerIdsRacksHigher = []

def getHostTopology():
    res = subprocess.check_output(["maprcli", "node", "list", "-columns", "racktopo", "-json"])
    maprclijson = json.loads(res)
    res = {}
    for host in maprclijson['data']:
        hostname = host['hostname']
        racktopo = host['racktopo']
        idx = racktopo.find("/" + hostname)
        res[hostname] = racktopo[:idx]
    return res


def getHostname(replica):
    colonidx = replica.find(':')
    name, alias, addresslist = socket.gethostbyaddr(replica[:colonidx])
    return name


def getVolumeRackPath(volumename):
    res = subprocess.check_output(["maprcli", "volume", "info", "-name", volumename, "-json"])
    maprclijson = json.loads(res)
    return maprclijson['data'][0]['rackpath']


def getVolumeDataDistribution(volumename, hostTopology):
    cliproc = subprocess.check_output(["maprcli", "dump", "volumeinfo", "-volumename", volumename, "-json"])
    res = VolumeDataDistribution(volumename)
    maprclijson = json.loads(cliproc)
    volumerackpath = getVolumeRackPath(volumename)
    for container in maprclijson['data']:
        if 'ContainerId' in container:
            containerId = str(container['ContainerId'])
            ipPorts = container['ActiveServers']['IP:Port']
            if not isinstance(ipPorts, list):
                ipPorts = [ipPorts]
            topoSet = set()
            for replica in ipPorts:
                hostname = getHostname(replica)
                rackName = hostTopology[hostname]
                topoIdx = rackName.find(volumerackpath)
                if topoIdx == 0:
                    topoSet.add(rackName)
                    res.affectedRacks.add(rackName)
                else:
                    res.outOfTopologyContainerIdsReplicas.append(containerId)
            numRacks = len(topoSet)
            if numRacks == 0:
                res.outOfTopologyContainerIdsContainers.append(containerId)
            elif numRacks == 1:
                res.topologyContainerIdsRacks1.append(containerId)
            elif numRacks == 2:
                res.topologyContainerIdsRacks2.append(containerId)
            elif numRacks == 3:
                res.topologyContainerIdsRacks3.append(containerId)
            elif numRacks == 4:
                res.topologyContainerIdsRacks4.append(containerId)
            elif numRacks == 5:
                res.topologyContainerIdsRacks5.append(containerId)
            elif numRacks == 6:
                res.topologyContainerIdsRacks6.append(containerId)
            else:
                res.topologyContainerIdsRacksHigher.append(containerId)
    return res

def printVolumeDataDistributionFormated(volumename, hostTopology):
    volumerackpath = getVolumeRackPath(volumename)
    distribution = getVolumeDataDistribution(volumename, hostTopology)
    print " "
    print "=========== VOLUME: " + volumename + " ======================"
    print " "
    print "   Volume rack path: " + volumerackpath
    print "   Data in racks: "
    for topologyRack in distribution.affectedRacks:
        print "         " + topologyRack
    print " "
    print "   Number of containers with no replica in assigned topology: " + str(len(distribution.outOfTopologyContainerIdsContainers))
    print "   Number of containers replicas outside of topology:         " + str(len(distribution.outOfTopologyContainerIdsReplicas))
    print "   Number of containers having replicas in 1 rack:            " + str(len(distribution.topologyContainerIdsRacks1))
    print "   Number of containers having replicas in 2 racks:           " + str(len(distribution.topologyContainerIdsRacks2))
    print "   Number of containers having replicas in 3 racks:           " + str(len(distribution.topologyContainerIdsRacks3))
    print "   Number of containers having replicas in 4 racks:           " + str(len(distribution.topologyContainerIdsRacks4))
    print "   Number of containers having replicas in 5 racks:           " + str(len(distribution.topologyContainerIdsRacks5))
    print "   Number of containers having replicas in 6 racks:           " + str(len(distribution.topologyContainerIdsRacks6))
    print "   Number of containers having replicas in more racks:        " + str(len(distribution.topologyContainerIdsRacksHigher))
    print " "
    print "   Containers with no replica in assigned topology: "
    print "     [" + str.join(', ', distribution.outOfTopologyContainerIdsContainers) + "]"
    print "   Container replicas outside of topology:          "
    print "     [" + str.join(', ', distribution.outOfTopologyContainerIdsReplicas) + "]"
    print "   Containers having replicas in 1 rack:            "
    print "     [" + str.join(', ', distribution.topologyContainerIdsRacks1) + "]"
    print "   Containers having replicas in 2 racks:           "
    print "     [" + str.join(', ', distribution.topologyContainerIdsRacks2) + "]"
    print "   Containers having replicas in 3 racks:           "
    print "     [" + str.join(', ', distribution.topologyContainerIdsRacks3) + "]"
    print "   Containers having replicas in 4 racks:           "
    print "     [" + str.join(', ', distribution.topologyContainerIdsRacks4) + "]"
    print "   Containers having replicas in 5 racks:           "
    print "     [" + str.join(', ', distribution.topologyContainerIdsRacks5) + "]"
    print "   Containers having replicas in 6 racks:           "
    print "     [" + str.join(', ', distribution.topologyContainerIdsRacks6) + "]"
    print "   Containers having replicas in more racks:        "
    print "     [" + str.join(', ', distribution.topologyContainerIdsRacksHigher) + "]"
    print " "


def getNonLocalVolumes():
    res = subprocess.check_output(["maprcli", "volume", "list", "-json"])
    maprclijson = json.loads(res)
    res = set()
    for volume in maprclijson['data']:
        if not 'localpath' in volume and ".local." not in volume['volumename']:
            res.add(volume['volumename'])
    return res


# ====================================
volumes = getNonLocalVolumes()
hostTopology = getHostTopology()
# print volumes
for volume in volumes:
    printVolumeDataDistributionFormated(volume, hostTopology)
