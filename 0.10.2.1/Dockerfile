FROM mbe1224/debian-oracle-java:stretch-slim-jdk8

ENV LANG="C.UTF-8" \
    KAFKA_DATA_DIR="/var/lib/kafka/data" \
    KFKA_HOME="/opt/kafka"

ARG PYTHON_VERSION=2.7.13-2
ARG PYTHON_PIP_VERSION=9.0.1
ARG KAFKA_VERSION=0.10.2.1
ARG KAFKA_DIST=kafka_2.11-${KAFKA_VERSION}
ARG KAFKA_SHA256_SUM=b86f75c8f078bc818031568155dd442ba6c1ed849663d0a7da9870efc96be461

EXPOSE 9092

RUN echo "===> Updating debian ....." && \
    apt-get -qq update && \
    echo "===> Installing curl wget netcat python...." && \
    apt-get install -y apt-transport-https curl wget netcat python=${PYTHON_VERSION} && \
    echo "===> Installing python packages ..."  && \
    curl -fSL "https://bootstrap.pypa.io/get-pip.py" | python && \
    pip install --no-cache-dir --upgrade pip==${PYTHON_PIP_VERSION} && \
    pip install --no-cache-dir jinja2 requests && \
    echo "===> Downloading kafka ..."  && \
    wget -q "http://www.apache.org/dist/kafka/${KAFKA_VERSION}/${KAFKA_DIST}.tgz" && \
    echo "===> Verifying kafka ..."  && \
    echo "${KAFKA_SHA256_SUM}" "${KAFKA_DIST}.tgzz" | sha256sum -c - && \    
    wget -q "http://www.apache.org/dist/kafka/${KAFKA_VERSION}/${KAFKA_DIST}.tgz.asc" && \
    wget -q "http://kafka.apache.org/KEYS" && \
    export GNUPGHOME="$(mktemp -d)" && \
    gpg --import KEYS && \
    gpg --batch --verify "${KAFKA_DIST}.tgz.asc" "${KAFKA_DIST}.tgz" && \
    echo "===> Unpacking kafka ..."  && \
    tar -xvf "${KAFKA_DIST}.tgzz" -C /opt && \
    rm -r "$GNUPGHOME" "${KAFKA_DIST}.tgz" "${KAFKA_DIST}.tgz.asc" && \
    echo "===> Shortcut created for install folder ..."  && \
    ln -s /opt/$KAFKA_DIST /opt/kafka && \
    ln -s /opt/kafka/bin/* /usr/bin && \
    echo "===> Removing extra files ..."  && \
    rm -rf  "/opt/kafka/bin/windows" \
            "/opt/kafka/site-docs/"*.cmd \
            "/opt/kafka/Notice"  && \
    apt-get autoremove -y wget && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir -p $KAFKA_DATA_DIR

COPY "/include/opt/kafka/tools/templates/"*.template /opt/kafka/tools/templates/
COPY "/include/opt/kafka/tools/"*.sh /opt/kafka/tools/
COPY /include/usr/local/bin/cub.py /usr/local/bin/cub
COPY /include/usr/local/bin/dub.py /usr/local/bin/dub

RUN chmod a+x "/opt/kafka/tools/"*.sh && \
    chmod a+x "usr/local/bin/cub" && \
    chmod a+x "usr/local/bin/dub"

CMD ["/opt/kafka/tools/run.sh"]