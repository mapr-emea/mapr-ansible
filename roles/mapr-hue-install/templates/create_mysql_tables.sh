#!/bin/bash

cd /opt/mapr/hue/hue-{{ version_output.stdout }}
source ./build/env/bin/activate
# somehow broken link on Redhat 7.3
pip uninstall -y MySQL-python
sleep 10
pip install MySQL-python
pip install MySQL-python
sleep 20
hue syncdb --noinput
hue migrate
deactivate