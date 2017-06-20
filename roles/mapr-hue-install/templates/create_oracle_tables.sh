#!/bin/bash

cd {{ hue_path_result.files[0].path }}
source ./build/env/bin/activate
export LD_LIBRARY_PATH="{{ oracle_version_arch_path.files[0].path }}/lib/libclntsh.so:$LD_LIBRARY_PATH"
pip install /tmp/cx_Oracle-5.3.tar.gz
hue syncdb --noinput
hue migrate
deactivate