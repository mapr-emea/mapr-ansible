#!/bin/bash

cd {{ hue_path_result.files[0].path }}
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