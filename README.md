# avro-test

This repository contains code to test the [Avro Serialization](https://avro.apache.org/) framework in Python3.
The Avro library for Python 3 has slightly different commands to Python 2, so bear that in mind when trying to run the project.

# Contents

`avro_tutorial.py` contains very basic code to test Avro (the same one provided on the Avro documentation).
It takes the schema in `schemas/test.avsc`, serializes objects according to that schema, writes them to a file in `serialized_data/avro_tutorial`, and then reads the file and deserializes the data again.

`avro_kafka_csi_producer.py` is a script that consumes a set of events from a configurable [Kafka](https://kafka.apache.org/) stream (properties obtained from config.ini), tries to serialize these events according to the schema in `schemas/customer_status_changes.avsc`,
and on success, sends the serialized event to a configurable Kafka Producer.

`avro_kafka_csi_consumer.py` is a script that consumes serialized events from the same Kafka queue to which `avro_kafka_csi_producer.py` writes, deserializes them according to the schema in `schemas/customer_status_changes.avsc`,
and prints the result.

`flume.properties` is an example configuration for a [Flume](https://flume.apache.org/) agent consuming avro serialized events from Kafka and storing them to a file with a `.avro` extension. This Flume agent has not been successfully tested yet.