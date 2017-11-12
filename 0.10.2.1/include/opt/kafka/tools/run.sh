#!/usr/bin/env bash

set -o nounset \
    -o errexit \
    -o verbose \
    -o xtrace

echo "===> ENV Variables ..."
env | sort

echo "===> User"
id

echo "===> Configuring ..."
/opt/kafka/tools/configure.sh

echo "===> Running preflight checks ... "
/opt/kafka/tools/ensure.sh

echo "===> Launching ... "
exec /opt/kafka/tools/launch.sh
