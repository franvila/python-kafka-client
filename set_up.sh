#!/usr/bin/env bash
set -xe

DOCKER_CMD="${DOCKER_CMD:-docker}"
GIT_URL="https://github.com/confluentinc/confluent-kafka-python"

LIBRDKAFKA_VERSION=$(git ls-remote --tags --refs --sort='version:refname' $GIT_URL v\[0-9]{1,}.[0-9]{1,}.[0-9]{1,} | tail -n1 | sed 's/.*\///')

echo "Using librdkafka version ${LIBRDKAFKA_VERSION}"

${DOCKER_CMD} build -t kroxylicious/pythonkafkaclient --build-arg LIBRDKAFKA_VERSION=$LIBRDKAFKA_VERSION .

${DOCKER_CMD} push kroxylicious/pythonkafkaclient:latest quay.io/fvila/pythonkafkaclient:latest
