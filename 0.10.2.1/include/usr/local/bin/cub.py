#!/usr/bin/env python

"""Confluent utility belt.

This script contains a set of utility functions required for running the
Confluent platform on docker.

The script supports following commands:

1. kafka-ready : Ensures a Kafka cluster is ready to accept client requests.
2. zk-ready: Ensures that a Zookeeper ensemble is ready to accept client requests.
3. listeners: Derives the listeners property from advertised.listeners.

These commands log any output to stderr and returns with exitcode 0 if successful, 1 otherwise.

"""
from __future__ import print_function
import os
import sys
import socket
import time
from contextlib import closing
import collections
import time
import json
import re
import requests
import subprocess


def wait_for_service(host, port, timeout):
    """Waits for a service to start listening on a port.

    Args:
        host: Hostname where the service is hosted.
        port: Port where the service is expected to bind.
        timeout: Time in secs to wait for the service to be available.

    Returns:
        False, if the timeout expires and the service is unreachable, True otherwise.

    """
    start = time.time()
    while True:
        try:
            s = socket.create_connection((host, int(port)), float(timeout))
            s.close()
            return True
        except socket.error:
            pass

        time.sleep(1)
        if time.time() - start > timeout:
            return False


def check_zookeeper_ready(connect_string, timeout):
    """Waits for a Zookeeper ensemble be ready. This commands uses the Java
       docker-utils library to get the Zookeeper status.
       This command supports a secure Zookeeper cluster. It expects the KAFKA_OPTS
       enviornment variable to contain the JAAS configuration.

    Args:
        connect_string: Zookeeper connection string (host:port, ....)
        timeout: Time in secs to wait for the Zookeeper to be available.

    Returns:
        False, if the timeout expires and Zookeeper is unreachable, True otherwise.

    """
    cmd_template = """
             java {jvm_opts} \
                 -cp /opt/kafka/tools/docker-utils.jar \
                 io.confluent.admin.utils.cli.ZookeeperReadyCommand \
                 {connect_string} \
                 {timeout_in_ms}"""

    # This is to ensure that we include KAFKA_OPTS only if the jaas.conf has
    # entries for zookeeper. If you enable SASL, it is recommended that you
    # should enable it for all the components. This is an option if SASL
    # cannot be enabled on Zookeeper.
    jvm_opts = ""
    is_zk_sasl_enabled = os.environ.get("ZOOKEEPER_SASL_ENABLED") or ""

    if (not is_zk_sasl_enabled.upper() == "FALSE") and os.environ.get("KAFKA_OPTS"):
        jvm_opts = os.environ.get("KAFKA_OPTS")

    cmd = cmd_template.format(
        jvm_opts=jvm_opts or "",
        connect_string=connect_string,
        timeout_in_ms=timeout * 1000)

    return subprocess.call(cmd, shell=True) == 0


def check_kafka_ready(expected_brokers, timeout, config, bootstrap_broker_list=None, zookeeper_connect=None, security_protocol=None):
    """Waits for a Kafka cluster to be ready and have at least the
       expected_brokers to present. This commands uses the Java docker-utils
       library to get the Kafka status.

       This command supports a secure Kafka cluster. If SSL is enabled, it
       expects the client_properties file to have the relevant SSL properties.
       If SASL is enabled, the command expects the JAAS config to be present in the
       KAFKA_OPTS environment variable and the SASL properties to present in the
       client_properties file.


    Args:
        expected_brokers: expected number of brokers in the cluster.
        timeout: Time in secs to wait for the Zookeeper to be available.
        config: properties file with client config for SSL and SASL.
        security_protocol: Security protocol to use.
        bootstrap_broker_list: Kafka bootstrap broker list string (host:port, ....)
        zookeeper_connect: Zookeeper connect string.

    Returns:
        False, if the timeout expires and Kafka cluster is unreachable, True otherwise.

    """
    cmd_template = """
             java {jvm_opts} \
                 -cp /opt/kafka/tools/docker-utils.jar \
                 io.confluent.admin.utils.cli.KafkaReadyCommand \
                 {expected_brokers} \
                 {timeout_in_ms}"""

    cmd = cmd_template.format(
        jvm_opts=os.environ.get("KAFKA_OPTS") or "",
        bootstrap_broker_list=bootstrap_broker_list,
        expected_brokers=expected_brokers,
        timeout_in_ms=timeout * 1000)

    if config:
        cmd = "{cmd} --config {config_path}".format(cmd=cmd, config_path=config)

    if security_protocol:
        cmd = "{cmd} --security-protocol {protocol}".format(cmd=cmd, protocol=security_protocol)

    if bootstrap_broker_list:
        cmd = "{cmd} -b {broker_list}".format(cmd=cmd, broker_list=bootstrap_broker_list)
    else:
        cmd = "{cmd} -z {zookeeper_connect}".format(cmd=cmd, zookeeper_connect=zookeeper_connect)

    exit_code = subprocess.call(cmd, shell=True)

    if exit_code == 0:
        return True
    else:
        return False


def get_kafka_listeners(advertised_listeners):
    """Derives listeners property from advertised.listeners. It just converts the
       hostname to 0.0.0.0 so that Kafka process listens to all the interfaces.

       For example, if
            advertised_listeners = PLAINTEXT://foo:9999,SSL://bar:9098, SASL_SSL://10.0.4.5:7888
            then, the function will return
            PLAINTEXT://0.0.0.0:9999,SSL://0.0.0.0:9098, SASL_SSL://0.0.0.0:7888

    Args:
        advertised_listeners: advertised.listeners string.

    Returns:
        listeners string.

    """
    host = re.compile(r'://(.*?):', re.UNICODE)
    return host.sub(r'://0.0.0.0:', advertised_listeners)


if __name__ == '__main__':

    import argparse
    root = argparse.ArgumentParser(description='Confluent Platform Utility Belt.')

    actions = root.add_subparsers(help='Actions', dest='action')

    zk = actions.add_parser('zk-ready', description='Check if ZK is ready.')
    zk.add_argument('connect_string', help='Zookeeper connect string.')
    zk.add_argument('timeout', help='Time in secs to wait for service to be ready.', type=int)

    kafka = actions.add_parser('kafka-ready', description='Check if Kafka is ready.')
    kafka.add_argument('expected_brokers', help='Minimum number of brokers to wait for', type=int)
    kafka.add_argument('timeout', help='Time in secs to wait for service to be ready.', type=int)
    kafka_or_zk = kafka.add_mutually_exclusive_group(required=True)
    kafka_or_zk.add_argument('-b', '--bootstrap_broker_list', help='List of bootstrap brokers.')
    kafka_or_zk.add_argument('-z', '--zookeeper_connect', help='Zookeeper connect string.')
    kafka.add_argument('-c', '--config', help='Path to config properties file (required when security is enabled).')
    kafka.add_argument('-s', '--security-protocol', help='Security protocol to use when multiple listeners are enabled.')

    config = actions.add_parser('listeners', description='Get listeners value from advertised.listeners. Replaces host to 0.0.0.0')
    config.add_argument('advertised_listeners', help='advertised.listeners string.')

    if len(sys.argv) < 2:
        root.print_help()
        sys.exit(1)

    args = root.parse_args()

    success = False

    if args.action == "zk-ready":
        success = check_zookeeper_ready(args.connect_string, int(args.timeout))
    elif args.action == "kafka-ready":
        success = check_kafka_ready(int(args.expected_brokers), int(args.timeout), args.config, args.bootstrap_broker_list, args.zookeeper_connect, args.security_protocol)
    elif args.action == "listeners":
        listeners = get_kafka_listeners(args.advertised_listeners)
        if listeners:
            # Print the output to stdout. Don't delete this, this is not for debugging.
            print(listeners)
            success = True

    if success:
        sys.exit(0)
    else:
        sys.exit(1)
