import os
import io
import json
import configparser

from kafka import KafkaConsumer, KafkaProducer

import avro.schema
from avro.io import AvroTypeException
from avro.io import DatumReader, DatumWriter
from avro.io import BinaryEncoder


if __name__ == "__main__":

    config = configparser.ConfigParser()
    config.read("config.ini")

    kafka_live_brokers = config['Kafka']['consumer brokers'].split(';')

    consumer = KafkaConsumer(config['Kafka']['consumer topic'],
                             group_id=config['Kafka']['consumer group'],
                             bootstrap_servers=kafka_live_brokers,
                             auto_offset_reset='earliest',
                             enable_auto_commit=False,
                             value_deserializer=lambda m: json.loads(m.decode('utf-8')))

    local_brokers = config['Kafka']['producer brokers'].split(';')

    schema_file = os.path.join("schemas", "customer_status_changes.avsc")
    schema = avro.schema.Parse(open(schema_file, "rb").read().decode("utf-8"))
    avro_writer = DatumWriter(schema)
    bytes_writer = io.BytesIO()
    encoder = BinaryEncoder(bytes_writer)

    avro_producer = KafkaProducer(bootstrap_servers=local_brokers)

    i = 0
    for message in consumer:
        try:
            avro_writer.write(message.value, encoder)
            raw_bytes = bytes_writer.getvalue()
            avro_producer.send(config['Kafka']['producer topic'], raw_bytes)
            print("New message sent to queue")
        except AvroTypeException:
            print("Error encoding message: ")
            print(message.value)

        i += 1
        if i == 300:
            break
