FROM mbe1224/debian-oracle-java:stretch-slim-jdk8

ENV LANG="C.UTF-8" \
    KAFKA_LOG_DIRS="/var/lib/kafka/data" \
    KAFKA_HOME="/opt/kafka"

ARG PYTHON_VERSION=2.7.13-2
ARG PYTHON_PIP_VERSION=9.0.1
ARG KAFKA_VERSION=0.11.0.1
ARG KAFKA_DIST=kafka_2.11-${KAFKA_VERSION}
ARG KAFKA_SHA256_SUM=0da77e1e542cf097d6025309bc996c10ceda394839c041934b86d8729ab574f1

EXPOSE 9092

RUN echo "===> Updating debian ....." && \
    apt-get -qq update && \
    echo "===> Installing gnupg2 curl wget netcat python...." && \
    apt-get install -y apt-transport-https gnupg2 curl wget netcat python=${PYTHON_VERSION} && \
    echo "===> Installing python packages ..."  && \
    curl -fSL "https://bootstrap.pypa.io/get-pip.py" | python && \
    pip install --no-cache-dir --upgrade pip==${PYTHON_PIP_VERSION} && \
    pip install --no-cache-dir jinja2 requests && \
    echo "===> Downloading kafka ..."  && \
    wget -q "http://archive.apache.org/dist/kafka/${KAFKA_VERSION}/${KAFKA_DIST}.tgz" && \
    echo "===> Verifying kafka ..."  && \
    echo "${KAFKA_SHA256_SUM}" "${KAFKA_DIST}.tgz" | sha256sum -c - && \    
    wget -q "http://archive.apache.org/dist/kafka/${KAFKA_VERSION}/${KAFKA_DIST}.tgz.asc" && \
    wget -q "http://kafka.apache.org/KEYS" && \
    export GNUPGHOME="$(mktemp -d)" && \
    gpg --import KEYS && \
    gpg --batch --verify "${KAFKA_DIST}.tgz.asc" "${KAFKA_DIST}.tgz" && \
    echo "===> Unpacking kafka ..."  && \
    tar -xvf "${KAFKA_DIST}.tgz" -C /opt && \
    rm -rf "${GNUPGHOME}" "${KAFKA_DIST}.tgz" "${KAFKA_DIST}.tgz.asc" && \
    echo "===> Shortcut created for install folder ..."  && \
    ln -s /opt/$KAFKA_DIST /opt/kafka && \
    ln -s /opt/kafka/bin/* /usr/bin && \
    echo "===> Removing extra files ..."  && \
    rm -rf  "/opt/kafka/bin/windows" \
            "/opt/kafka/site-docs" \
            "/opt/kafka/NOTICE"  && \
    apt-get autoremove -y gnupg2 wget && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir -p $KAFKA_LOG_DIRS /opt/kafka/secrets

COPY "/include/opt/kafka/tools/templates/"*.template /opt/kafka/tools/templates/
COPY "/include/opt/kafka/tools/"*.* /opt/kafka/tools/
COPY /include/usr/local/bin/cub.py /usr/local/bin/cub
COPY /include/usr/local/bin/dub.py /usr/local/bin/dub

RUN chmod a+x "/opt/kafka/tools/"*.sh && \
    chmod a+x "usr/local/bin/cub" && \
    chmod a+x "usr/local/bin/dub"

CMD ["/opt/kafka/tools/run.sh"]