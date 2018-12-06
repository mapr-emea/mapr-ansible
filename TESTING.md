# Testing mapr-ansible roles

## Introduction

Tests are based on molecule framework
* https://molecule.readthedocs.io/
* https://github.com/metacloud/molecule

## Requirements

* Docker

## Run linter

docker run --rm -it \
    -v "$(pwd)":/tmp/$(basename "${PWD}"):ro \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -w /tmp/$(basename "${PWD}") \
    retr0h/molecule:latest \
    molecule test -s lint

