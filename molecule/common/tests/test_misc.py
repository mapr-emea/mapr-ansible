import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_mc_installed(host):
    p = host.package("mc")

    assert p.is_installed


def test_wget_installed(host):
    p = host.package("wget")

    assert p.is_installed


def test_mysql_python_installed(host):
    p = host.package("MySQL-python")

    assert p.is_installed


def test_openssl_installed(host):
    p = host.package("openssl")

    assert p.is_installed
