#
# Copyright Kroxylicious Authors.
#
# Licensed under the Apache Software License version 2.0, available at http://www.apache.org/licenses/LICENSE-2.0
#

FROM alpine:edge

COPY . /usr/src/confluent-kafka-python

ARG LIBRDKAFKA_VERSION

ENV BUILD_DEPS="git make gcc g++ pkgconfig python3-dev"

ENV RUN_DEPS="bash librdkafka-dev>${LIBRDKAFKA_VERSION} libcurl cyrus-sasl-gssapiv2 ca-certificates libsasl heimdal-libs krb5 zstd-libs zstd-static python3 py3-pip"

RUN \
    apk update && \
    apk add --no-cache --virtual .dev_pkgs $BUILD_DEPS && \
    apk add --no-cache $RUN_DEPS && \
    echo Installing confluent-kafka-python && \
    python3 -m pip install -I confluent_kafka==${LIBRDKAFKA_VERSION} --break-system-packages && \
    apk del .dev_pkgs

RUN \
    python3 -c 'import confluent_kafka as cf ; print(cf.version(), "librdkafka", cf.libversion())'
