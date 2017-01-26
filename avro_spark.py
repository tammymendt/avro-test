import os

from pyspark import SparkContext
from pyspark import SQLContext


SPARK_AVRO_FORMAT = "com.databricks.spark.avro"

if __name__ == "__main__":

    sc = SparkContext(appName="test avro")
    sql_context = SQLContext(sc)

    current_dir = os.path.dirname(os.path.realpath(__file__))

    df = sql_context.read.format(SPARK_AVRO_FORMAT).load(
        'file://' + os.path.join(current_dir, 'serialized_data'))

    df.show()

    sc.stop()

