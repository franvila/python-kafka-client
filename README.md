# Python Kafka Client

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
-k          optional parameters to set the message key
```

```bash
kubectl run -i -n <namespace> --image=quay.io/fvila/pythonkafkaclient:2.11.1 -- python3 /usr/src/confluent-kafka-python/Producer.py -b <bootstrap-servers> -t <topic_name>
```

### Consumer

The different parameters that can be used are:
```
-b          list of boostrap servers separated by coma
-t          topic name
-n          number of messages expected to receive
-g          optional parameters to set the group name
```
```bash
kubectl run -i -n <namespace> --image=quay.io/fvila/pythonkafkaclient:2.11.1 -- python3 /usr/src/confluent-kafka-python/Consumer.py -n <num_of_expected_messages> -b <bootstrap-servers> -t <topic_name>
```
