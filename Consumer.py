#
# Copyright Kroxylicious Authors.
#
# Licensed under the Apache Software License version 2.0, available at http://www.apache.org/licenses/LICENSE-2.0
#

from confluent_kafka import Consumer, KafkaException
import argparse
import sys
import logging

def print_record(msg):
    key = "" if msg.key() is None else str(msg.key().decode("utf-8"))
    headers = "["
    if msg.headers() is not None:
        for header in msg.headers():
            headers += "{\"" + header[0] + "\":\"" + str(header[1].decode("utf-8")) + "\"},"
        headers = headers[:-1]
    headers += "]"
    sys.stdout.write("Received: {\"name\":\"record_data\",\"topic\":\"%s\",\"partition\":%d,\"key\":\"%s\",\"payload\":\"%s\",\"offset\":%d,\"headers\":%s}\n" %
                     (msg.topic(), msg.partition(), key, msg.value().decode("utf-8"), msg.offset(), headers))

def main(args):
    topic = args.topic
    records_expected = int(args.num_of_records)
    # Consumer configuration
    # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    conf = {'bootstrap.servers': args.bootstrap_servers, 'group.id': args.group, 'session.timeout.ms': 6000,
            'auto.offset.reset': 'earliest', 'enable.auto.offset.store': False}


    # Create logger for consumer (logs will be emitted when poll() is called)
    logger = logging.getLogger('consumer')
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(asctime)-15s %(levelname)-8s %(message)s'))
    logger.addHandler(handler)

    # Create Consumer instance
    # Hint: try debug='fetch' to generate some log records
    c = Consumer(conf, logger=logger)

    def print_assignment(consumer, partitions):
        print('Assignment:', partitions)

    # Subscribe to topics
    c.subscribe([topic], on_assign=print_assignment)

    # Read records from Kafka, print to stdout
    try:
        records_received = 0
        while True:
            msg = c.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                raise KafkaException(msg.error())
            else:
                print_record(msg)
                # Store the offset associated with msg to a local cache.
                # Stored offsets are committed to Kafka by a background thread every 'auto.commit.interval.ms'.
                # Explicitly storing offsets after processing gives at-least once semantics.
                c.store_offsets(msg)
                records_received += 1
            if records_received == records_expected:
                c.close()
                sys.exit(0)

    except KeyboardInterrupt:
        sys.stderr.write('%% Aborted by user\n')

    finally:
        # Close down consumer to commit final offsets.
        c.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Consumer")
    parser.add_argument('-b', dest="bootstrap_servers", required=True,
                        help="Bootstrap broker(s) (host[:port])")
    parser.add_argument('-n', dest="num_of_records",
                        help="Number of records expected")
    parser.add_argument('-t', dest="topic", required=True,
                        help="Topic name")
    parser.add_argument('-g', dest="group",
                        help="Consumer group")

    main(parser.parse_args())
