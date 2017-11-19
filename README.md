## Docker [Kafka] image using [Oracle JDK] ##

### Supported tags and respective Dockerfile links: ###

* ```0.10.2.1``` _\([0.10.2.1/Dockerfile]\)_
[![](https://images.microbadger.com/badges/image/mbe1224/kafka:0.10.2.1.svg)](https://microbadger.com/images/mbe1224/kafka:0.10.2.1 "")
* ```0.11.0.1``` _\([0.11.0.1/Dockerfile]\)_
[![](https://images.microbadger.com/badges/image/mbe1224/kafka:0.11.0.1.svg)](https://microbadger.com/images/mbe1224/kafka:0.11.0.1 "")
* ```0.11.0.2``` _\([0.11.0.2/Dockerfile]\)_
[![](https://images.microbadger.com/badges/image/mbe1224/kafka:0.11.0.2.svg)](https://microbadger.com/images/mbe1224/kafka:0.11.0.2 "")
* ```1.0.0```, ```latest``` _\([1.0.0/Dockerfile]\)_
[![](https://images.microbadger.com/badges/image/mbe1224/kafka:1.0.0.svg)](https://microbadger.com/images/mbe1224/kafka:1.0.0 "")

### Summary: ###

- Debian "slim" image variant
- Oracle JDK 8u152 addded, without MissionControl, VisualVM, JavaFX, ReadMe files, source archives, etc.
- Oracle Java Cryptography Extension added
- Python 2.7.9-1 & pip 9.0.1 added
- Verified downloads
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
    mbe1224/kafka
```

### Configuration: ###

One can configure a Kafka instance using environment variables. All [Configuration Options] \([Broker Configs] and [Topic-level Configs]\) from the official documentation can be used as long as the following naming rules are followed:
- upper caps
- "." replaced with "\_"
- snake case instead of pascal case
- "KAFKA\_" prefix

For example, in order to set the replication factor for the offsets topic, one has to modifiy the "offsets.topic.replication.factor" property, which is translated in the "KAFKA\_OFFSETS\_TOPIC\_REPLICATION\_FACTOR" environment variable.

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
   [0.11.0.2/Dockerfile]: <https://github.com/MihaiBogdanEugen/docker-kafka/blob/master/0.11.0.2/Dockerfile>
   [1.0.0/Dockerfile]: <https://github.com/MihaiBogdanEugen/docker-kafka/blob/master/1.0.0/Dockerfile>
   [MIT License]: <https://raw.githubusercontent.com/MihaiBogdanEugen/docker-kafka/master/LICENSE>
   [Oracle Binary Code License Agreement]: <https://raw.githubusercontent.com/MihaiBogdanEugen/docker-kafka/master/Oracle_Binary_Code_License_Agreement%20for%20the%20Java%20SE%20Platform_Products_and_JavaFX>