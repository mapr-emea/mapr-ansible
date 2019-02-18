import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_sysctl_file(host):
    f = host.file('/etc/sysctl.conf')

    assert f.exists
    assert f.contains("vm.swappiness = 1")
    assert f.contains("net.ipv4.tcp_retries2 = 5")
    assert f.contains("vm.overcommit_memory = 0")
