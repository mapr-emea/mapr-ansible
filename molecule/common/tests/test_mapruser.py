import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_mapr_user(host):
    u = host.user('mapr')

    assert u.exists
    assert u.name == "mapr"
    assert u.group == "mapr"
    for g in ['mapr', 'root']:
        assert g in u.groups
    assert u.gid == 5000

    home = host.file("/home/mapr")

    assert home.is_directory
    assert home.user == "mapr"
    assert home.group == "mapr"
