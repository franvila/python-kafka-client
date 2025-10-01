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
-b          list of boostrap servers separated by coma
-t          topic name
-k          optional parameter to set the message key
-H          optional parameter to set a header in format 'header1=header value'. 
            If more than one header is added, -H has to be included multiple times: "-H 'header1=header1 value' -H 'header2=header2 value'..."
-X          Extra configuration used for SASL: 
              * sasl_mechanism=<value> --> SASL mechanism to use for authentication. Choices=['GSSAPI', 'PLAIN', 'SCRAM-SHA-512', 'SCRAM-SHA-256']
              * username=<value>       --> Username
              * user_secret=<value>    --> Password for PLAIN and SCRAM, or path to keytab (ignored on Windows) if GSSAPI.
--tls       Enables TLS when sasl_mechanism is configured
```

```bash
kubectl run -i -n <namespace> --image=quay.io/fvila/pythonkafkaclient:0.1.0-2.11.1 -- python3 /usr/src/confluent-kafka-python/Producer.py -b <bootstrap-servers> -t <topic_name>
```

### Consumer

The different parameters that can be used are:
```
-b          list of boostrap servers separated by coma
-t          topic name
-n          number of messages expected to receive
-g          optional parameters to set the group name
-X          Extra configuration used for SASL: 
              * sasl_mechanism=<value> --> SASL mechanism to use for authentication. Choices=['GSSAPI', 'PLAIN', 'SCRAM-SHA-512', 'SCRAM-SHA-256']
              * username=<value>       --> Username
              * user_secret=<value>    --> Password for PLAIN and SCRAM, or path to keytab (ignored on Windows) if GSSAPI.
--tls       Enables TLS when sasl_mechanism is configured
```
```bash
kubectl run -i -n <namespace> --image=quay.io/fvila/pythonkafkaclient:0.1.0-2.11.1 -- python3 /usr/src/confluent-kafka-python/Consumer.py -n <num_of_expected_messages> -b <bootstrap-servers> -t <topic_name>
```
