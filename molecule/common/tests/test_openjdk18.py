import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_java_installed(host):
    list = ['java-1.8.0-openjdk',
            'java-1.8.0-openjdk-devel',
            'java-1.8.0-openjdk-headless']
    for j in list:
        p = host.package(j)

        assert p.is_installed
