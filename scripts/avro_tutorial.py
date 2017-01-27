import os

import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter

if __name__ == "__main__":

    current_dir = os.path.dirname(os.path.realpath(__file__))
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

    schema_file = os.path.join(parent_dir, "schemas", "test.avsc")
    serialized_data_file = os.path.join(parent_dir, "serialized_data", "avro_tutorial", "test.avro")

    schema = avro.schema.Parse(open(schema_file, "rb").read().decode("utf-8"))

    writer = DataFileWriter(open(serialized_data_file, "wb"), DatumWriter(), schema)

    writer.append({"name": "Alyssa", "favorite_number": 256})
    writer.append({"name": "Ben", "favorite_number": 7, "favorite_color": "red"})
    writer.close()

    reader = DataFileReader(open(serialized_data_file, "rb"), DatumReader())

    for user in reader:
        print(user)

    reader.close()
