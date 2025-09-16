FROM alpine:3.22.1

COPY . /usr/src/confluent-kafka-python

ARG LIBRDKAFKA_VERSION="latest"

ENV BUILD_DEPS="git make gcc g++ curl pkgconfig bsd-compat-headers zlib-dev openssl-dev cyrus-sasl-dev curl-dev zstd-dev yajl-dev python3-dev"

ENV RUN_DEPS="bash libcurl cyrus-sasl-gssapiv2 ca-certificates libsasl heimdal-libs krb5 zstd-libs zstd-static yajl python3 py3-pip pipx"

RUN \
    apk update && \
    apk add --no-cache --virtual .dev_pkgs $BUILD_DEPS && \
    apk add --no-cache $RUN_DEPS

RUN \
    echo Installing librdkafka && \
    mkdir -p /usr/src/librdkafka && \
    cd /usr/src/librdkafka && \
    curl -LfsS https://github.com/edenhill/librdkafka/archive/${LIBRDKAFKA_VERSION}.tar.gz | \
        tar xvzf - --strip-components=1 && \
    ./configure --prefix=/usr --disable-lz4-ext && \
    make -j && \
    make install && \
    cd / && \
    rm -rf /usr/src/librdkafka

RUN \
    echo Installing confluent-kafka-python && \
    python3 -m pip install confluent_kafka --break-system-packages

RUN \
    apk del .dev_pkgs

RUN \
    python3 -c 'import confluent_kafka as cf ; print(cf.version(), "librdkafka", cf.libversion())' && \
    ls /usr/src/confluent-kafka-python
