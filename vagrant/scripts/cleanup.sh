#!/bin/bash

echo "debug: Executing scripts/cleanup.sh"

dd if=/dev/zero of=/EMPTY bs=1M
rm -f /EMPTY
sync
yum clean all
rm -rf /var/cache/yum