import os
import io
import configparser

from kafka import KafkaConsumer

import avro.schema
from avro.io import AvroTypeException
from avro.io import DatumReader
from avro.io import BinaryDecoder


if __name__ == "__main__":

    config = configparser.ConfigParser()
    config.read("config.ini")

    local_brokers = config['Kafka']['producer brokers'].split(';')

    consumer = KafkaConsumer(config['Kafka']['producer topic'],
                             group_id=config['Kafka']['consumer group'],
                             bootstrap_servers=local_brokers,
                             auto_offset_reset='earliest',
                             enable_auto_commit=False)

    current_dir = os.path.dirname(os.path.realpath(__file__))
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
    schema_file = os.path.join(parent_dir, "schemas", "customer_status_changes.avsc")
    schema = avro.schema.Parse(open(schema_file, "rb").read().decode("utf-8"))

    avro_reader = DatumReader(schema)

    for message in consumer:
        try:
            bytes_reader = io.BytesIO(message.value)
            decoder = BinaryDecoder(bytes_reader)
            value = avro_reader.read(decoder)
            print(value)
        except AvroTypeException:
            print("Error decoding message: ")
            raise
