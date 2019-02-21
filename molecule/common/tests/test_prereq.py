import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_pam_directory(host):
    f = host.file('/etc/pam.d/system-auth-pc')

    assert f.exists
    assert f.is_directory
