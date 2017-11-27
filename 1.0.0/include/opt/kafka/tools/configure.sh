#!/usr/bin/env bash

set -o nounset \
    -o errexit \
    -o verbose \
    -o xtrace

if [[ -n "${IS_KUBERNETES-}" ]]
then
  export KAFKA_BROKER_ID="${HOSTNAME##*-}"
else 
  dub ensure KAFKA_ADVERTISED_LISTENERS
  # By default, LISTENERS is derived from ADVERTISED_LISTENERS by replacing
  # hosts with 0.0.0.0. This is good default as it ensures that the broker
  # process listens on all ports.
  if [[ -z "${KAFKA_LISTENERS-}" ]]
  then
    export KAFKA_LISTENERS
    KAFKA_LISTENERS=$(cub listeners "$KAFKA_ADVERTISED_LISTENERS")
  fi
fi

dub ensure KAFKA_BROKER_ID
dub ensure KAFKA_ZOOKEEPER_CONNECT

if [[ -z "${KAFKA_LOG_DIRS-}" ]]
then
  export KAFKA_LOG_DIRS
  KAFKA_LOG_DIRS="/var/lib/kafka/data"
fi

# advertised.host, advertised.port, host and port are deprecated. Exit if these properties are set.
if [[ -n "${KAFKA_ADVERTISED_PORT-}" ]]
then
    echo "advertised.port is deprecated. Please use KAFKA_ADVERTISED_LISTENERS instead."
    exit 1
fi

if [[ -n "${KAFKA_ADVERTISED_HOST-}" ]]
then
  echo "advertised.host is deprecated. Please use KAFKA_ADVERTISED_LISTENERS instead."
  exit 1
fi

if [[ -n "${KAFKA_HOST-}" ]]
then
  echo "host is deprecated. Please use KAFKA_ADVERTISED_LISTENERS instead."
  exit 1
fi

if [[ -n "${KAFKA_PORT-}" ]]
then
  echo "port is deprecated. Please use KAFKA_ADVERTISED_LISTENERS instead."
  exit 1
fi

# Set if KAFKA_LISTENERS has SSL:// or SASL_SSL:// endpoints.
if [[ $KAFKA_LISTENERS == *"SSL://"* ]]
then
  echo "SSL is enabled."

  dub ensure KAFKA_SSL_KEYSTORE_FILENAME
  export KAFKA_SSL_KEYSTORE_LOCATION="/opt/kafka/secrets/$KAFKA_SSL_KEYSTORE_FILENAME"
  dub path "$KAFKA_SSL_KEYSTORE_LOCATION" exists

  dub ensure KAFKA_SSL_KEY_CREDENTIALS
  KAFKA_SSL_KEY_CREDENTIALS_LOCATION="/opt/kafka/secrets/$KAFKA_SSL_KEY_CREDENTIALS"
  dub path "$KAFKA_SSL_KEY_CREDENTIALS_LOCATION" exists
  export KAFKA_SSL_KEY_PASSWORD
  KAFKA_SSL_KEY_PASSWORD=$(cat "$KAFKA_SSL_KEY_CREDENTIALS_LOCATION")

  dub ensure KAFKA_SSL_KEYSTORE_CREDENTIALS
  KAFKA_SSL_KEYSTORE_CREDENTIALS_LOCATION="/opt/kafka/secrets/$KAFKA_SSL_KEYSTORE_CREDENTIALS"
  dub path "$KAFKA_SSL_KEYSTORE_CREDENTIALS_LOCATION" exists
  export KAFKA_SSL_KEYSTORE_PASSWORD
  KAFKA_SSL_KEYSTORE_PASSWORD=$(cat "$KAFKA_SSL_KEYSTORE_CREDENTIALS_LOCATION")

  dub ensure KAFKA_SSL_TRUSTSTORE_FILENAME
  export KAFKA_SSL_TRUSTSTORE_LOCATION="/opt/kafka/secrets/$KAFKA_SSL_TRUSTSTORE_FILENAME"
  dub path "$KAFKA_SSL_TRUSTSTORE_LOCATION" exists

  dub ensure KAFKA_SSL_TRUSTSTORE_CREDENTIALS
  KAFKA_SSL_TRUSTSTORE_CREDENTIALS_LOCATION="/opt/kafka/secrets/$KAFKA_SSL_TRUSTSTORE_CREDENTIALS"
  dub path "$KAFKA_SSL_TRUSTSTORE_CREDENTIALS_LOCATION" exists
  export KAFKA_SSL_TRUSTSTORE_PASSWORD
  KAFKA_SSL_TRUSTSTORE_PASSWORD=$(cat "$KAFKA_SSL_TRUSTSTORE_CREDENTIALS_LOCATION")
fi

# Set if KAFKA_LISTENERS has SASL_PLAINTEXT:// or SASL_SSL:// endpoints.
if [[ $KAFKA_LISTENERS =~ .*SASL_.*://.* ]]
then
  echo "SASL" is enabled.

  dub ensure KAFKA_OPTS

  if [[ ! $KAFKA_OPTS == *"java.security.auth.login.config"*  ]]
  then
    echo "KAFKA_OPTS should contain 'java.security.auth.login.config' property."
  fi
fi

if [[ -n "${KAFKA_JMX_OPTS-}" ]]
then
  if [[ ! $KAFKA_JMX_OPTS == *"com.sun.management.jmxremote.rmi.port"*  ]]
  then
    echo "KAFKA_OPTS should contain 'com.sun.management.jmxremote.rmi.port' property. It is required for accessing the JMX metrics externally."
  fi
fi

echo "===> Writing kafka.properties ..."
dub template "/opt/kafka/tools/templates/kafka.properties.template" "/opt/kafka/config/kafka.properties"

echo "===> Writing log4j.properties ..."
dub template "/opt/kafka/tools/templates/log4j.properties.template" "/opt/kafka/config/log4j.properties"

echo "===> Writing tools-log4j.properties ..."
dub template "/opt/kafka/tools/templates/tools-log4j.properties.template" "/opt/kafka/config/tools-log4j.properties"

export KAFKA_LOG_DIRS=${KAFKA_LOG_DIRS:-"/var/lib/kafka/data"}
echo "===> Check if $KAFKA_LOG_DIRS is writable ..."
dub path "$KAFKA_LOG_DIRS" writable

echo "===> Check if Zookeeper is healthy ..."
cub zk-ready "$KAFKA_ZOOKEEPER_CONNECT" "${KAFKA_CUB_ZK_TIMEOUT:-40}"