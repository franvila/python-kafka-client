# Python Kafka Test Client

The intent of this client is to help Kroxylicious system tests, so all configurations are made to fulfill our requirements.

## Usage

The essential requirement to run these clients is a Kubernetes cluster with an Apache Kafka cluster.

After successfully building images (which will cause the images to be pushed to the specified Docker repository) you are ready to deploy the producer and consumer containers along with Kafka.

You can deploy clients by using kubernetes `Jobs` with the example image.

Example command for deploying job:

### Producer

The different parameters that can be used are:
```
-b <bootstrap_servers>        list of boostrap servers separated by coma
-t <topic_name>               topic name
-k <key>                      optional parameter to set the message key
-H <headerKey=headerValue>    optional parameter to set a header. 
                              If more than one header is added, -H has to be included multiple times: "-H 'header1=header1 value' -H 'header2=header2 value'..."
-X <name=value>               Extra configuration (See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md)
                              If more than one extra config is added, -X has to be included multiple times
                                * sasl.mechanism=<value>    --> SASL mechanism to use for authentication. Choices=['GSSAPI', 'PLAIN', 'SCRAM-SHA-512', 'SCRAM-SHA-256']
                                * security.protocol=<value> --> Security protocol to use. Choices=['PLAINTEXT', 'SASL_PLAINTEXT', 'SSL', 'SASL_SSL']
                                * sasl.username=<value>     --> Username
                                ...
```

```bash
kubectl run -i -n <namespace> --image=quay.io/fvila/pythonkafkaclient:0.1.0-2.11.1 -- python3 /usr/src/confluent-kafka-python/Producer.py -b <bootstrap-servers> -t <topic_name>
```

### Consumer

The different parameters that can be used are:
```
-b <bootstrap_servers>        list of boostrap servers separated by coma
-t <topic_name>               topic name
-n <int>                      number of messages expected to receive
-g <group_name>               optional parameters to set the group name
-X <name=value>               Extra configuration (See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md)
                              If more than one extra config is added, -X has to be included multiple times
                                * sasl.mechanism=<value>    --> SASL mechanism to use for authentication. Choices=['GSSAPI', 'PLAIN', 'SCRAM-SHA-512', 'SCRAM-SHA-256']
                                * security.protocol=<value> --> Security protocol to use. Choices=['PLAINTEXT', 'SASL_PLAINTEXT', 'SSL', 'SASL_SSL']
                                * sasl.username=<value>     --> Username
                                ...
```
```bash
kubectl run -i -n <namespace> --image=quay.io/fvila/pythonkafkaclient:0.1.0-2.11.1 -- python3 /usr/src/confluent-kafka-python/Consumer.py -n <num_of_expected_messages> -b <bootstrap-servers> -t <topic_name>
```
