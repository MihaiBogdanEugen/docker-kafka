## Docker [Kafka] image using [Oracle JDK] ##

### Supported tags and respective Dockerfile links: ###

* ```0.10.2.1``` _\([0.10.2.1/Dockerfile]\)_
[![](https://images.microbadger.com/badges/image/mbe1224/kafka:0.10.2.1.svg)](https://microbadger.com/images/mbe1224/kafka:0.10.2.1 "")
* ```0.11.0.1``` _\([0.11.0.1/Dockerfile]\)_
[![](https://images.microbadger.com/badges/image/mbe1224/kafka:0.11.0.1.svg)](https://microbadger.com/images/mbe1224/kafka:0.11.0.1 "")
* ```1.0.0```, ```latest``` _\([1.0.0/Dockerfile]\)_
[![](https://images.microbadger.com/badges/image/mbe1224/kafka:1.0.0.svg)](https://microbadger.com/images/mbe1224/kafka:1.0.0 "")

### Summary: ###

- Debian "slim" image variant
- Oracle JDK 8u152 addded, without MissionControl, VisualVM, JavaFX, ReadMe files, source archives, etc.
- Oracle Java Cryptography Extension added
- Python 2.7.9-1 & pip 9.0.1 added
- SHA 256 sum checks for all downloads
- JAVA\_HOME environment variable set up
- Utility scripts added for generating the configuration files

### Usage: ###

Build the image
```shell
docker build -t mbe1224/kafka /1.0.0/
```

Run the container
```shell
docker run -d \
    --net=host \
    --name=kafka \
    -e KAFKA_ZOOKEEPER_CONNECT=localhost:2181 \
    -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092 \
    -e KAFKA_BROKER_ID=1 \
    -e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 \
    mbe1224/kafka
```

### Environment variables: ###

One can use the following environment variables for configuring the ZooKeeper node:

| # | Name | Default value | Meaning | Comments |
|---|---|---|---|---|
| 1 | KAFKA\_ADVERTISED\_LISTENERS | - | Advertised listeners is how it gives out a host name that can be reached by the client | - |
| 2 | KAFKA\_BROKER\_ID | - | Node identifier | Required in Kafka replicated scenarios |
| 3 | KAFKA\_CUB\_ZK\_TIMEOUT | 40 | Time in secondss to wait for the Zookeeper to be available | - |
| 4 | KAFKA\_JMX\_OPTS | - | JMX options used for monitoring | KAFKA\_OPTS should contain 'com.sun.management.jmxremote.rmi.port' property |
| 5 | KAFKA\_LOG4J\_LOGGERS | {'kafka': 'INFO','kafka.network.RequestChannel$': 'WARN','kafka.producer.async.DefaultEventHandler': 'DEBUG','kafka.request.logger': 'WARN','kafka.controller': 'TRACE','kafka.log.LogCleaner': 'INFO','state.change.logger': 'TRACE','kafka.authorizer.logger': 'WARN'} | - | - |
| 6 | KAFKA\_LOG4J\_ROOT\_LOGLEVEL | INFO | - | - |
| 7 | KAFKA\_OFFSETS\_TOPIC\_REPLICATION\_FACTOR | 3 | The replication factor for the offsets topic - set higher to ensure availability | Internal topic creation will fail until the cluster size meets this replication factor requirement |
| 8 | KAFKA\_SSL\_KEY\_CREDENTIALS | - | SSL key credentials | Required if SSL is enabled |
| 9 | KAFKA\_SSL\_KEYSTORE\_CREDENTIALS | - | SSL keystore credentials | Required if SSL is enabled |
| 10 | KAFKA\_SSL\_KEYSTORE\_FILENAME | - | SSL keystore filename | Required if SSL is enabled |
| 11 | KAFKA\_SSL\_TRUSTSTORE\_CREDENTIALS | - | SSL trustore credentials | Required if SSL is enabled |
| 12 | KAFKA\_SSL\_TRUSTSTORE\_FILENAME | - | SSL trustore filename | Required if SSL is enabled |
| 13 | KAFKA\_TOOLS\_LOG4J\_LOGLEVEL | WARN | - | - |
| 14 | KAFKA\_ZOOKEEPER\_CONNECT | - | Tells Kafka how to get in touch with ZooKeeper | - |

Moreover, one can use any of the properties specified in the [Configuration Options] \([Broker Configs] and [Topic-level Configs]\) by replacing "." with "\_" and appending "KAFKA\_" before the property name. For example, instead of ```offsets.topic.replication.factor``` use ```KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR```.

### Dual licensed under: ###

* [MIT License]
* [Oracle Binary Code License Agreement]

   [Oracle JDK]: <http://www.oracle.com/technetwork/java/javase/downloads/index.html>
   [Kafka]: <https://kafka.apache.org/> 
   [Apache Kafka]: <https://kafka.apache.org/>      
   [Configuration Options]: <https://kafka.apache.org/documentation/#configuration>
   [Broker Configs]: <https://kafka.apache.org/documentation/#brokerconfigs>
   [Topic-level Configs]: <https://kafka.apache.org/documentation/#topic-config>
   [0.10.2.1/Dockerfile]: <https://github.com/MihaiBogdanEugen/docker-kafka/blob/master/0.10.2.1/Dockerfile>
   [0.11.0.1/Dockerfile]: <https://github.com/MihaiBogdanEugen/docker-kafka/blob/master/0.11.0.1/Dockerfile>
   [1.0.0/Dockerfile]: <https://github.com/MihaiBogdanEugen/docker-kafka/blob/master/1.0.0/Dockerfile>
   [MIT License]: <https://raw.githubusercontent.com/MihaiBogdanEugen/docker-kafka/master/LICENSE>
   [Oracle Binary Code License Agreement]: <https://raw.githubusercontent.com/MihaiBogdanEugen/docker-kafka/master/Oracle_Binary_Code_License_Agreement%20for%20the%20Java%20SE%20Platform_Products_and_JavaFX>