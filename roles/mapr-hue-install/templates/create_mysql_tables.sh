#!/bin/bash

cd {{ hue_path_result.files[0].path }}
source ./build/env/bin/activate
# somehow broken link on Redhat 7.3
pip uninstall -y MySQL-python
pip install MySQL-python
hue syncdb --noinput
hue migrate
deactivate