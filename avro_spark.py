import os

from pyspark import SparkContext
from pyspark import SQLContext


SPARK_AVRO_FORMAT = "com.databricks.spark.avro"

os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages com.databricks:spark-avro_2.11:3.1.0 pyspark-shell'

if __name__ == "__main__":

    sc = SparkContext(appName="test avro")
    sql_context = SQLContext(sc)

    current_dir = os.path.dirname(os.path.realpath(__file__))

    df = sql_context.read.format(SPARK_AVRO_FORMAT).load(
        'file://' + os.path.join(current_dir, 'serialized_data', 'avro_tutorial'))

    df.show()

    sc.stop()

