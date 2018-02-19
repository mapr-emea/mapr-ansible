#!/bin/bash

cd /opt/mapr/hue/hue-{{ version_output.stdout }}
source ./build/env/bin/activate
#pip uninstall -y MySQL-python
pip install --upgrade --force-reinstall MySQL-python
hue syncdb --noinput
hue migrate
deactivate