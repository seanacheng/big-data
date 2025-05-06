#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
 Generates buy/sell signals for a stock.

 To run this on Halligan, open two terminals on the same server
    $ cd BigData/Quiz_7
    $ python new-stock-price-feeder.py | nc -lk 9999
    $ spark-submit 'structured-streaming-stock-signals.py' localhost 9999
"""
import sys
from pyspark.context import SparkContext
from pyspark.sql import SparkSession

from pyspark.sql.functions import *
from pyspark.sql.types import *

def setLogLevel(sc, level):
    from pyspark.sql import SparkSession
    spark = SparkSession(sc)
    spark.sparkContext.setLogLevel(level)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: structured-streaming-stock-signals.py <hostname> <port>", file=sys.stderr)
        sys.exit(-1)

    print ('Argv', sys.argv)
    
    host = sys.argv[1]
    port = int(sys.argv[2])
    print ('host', type(host), host, 'port', type(port), port)

    ctx = SparkContext(appName = "Stock Buy/Sell Signals")

    spark = SparkSession(ctx).builder.getOrCreate()
    sc = spark.sparkContext

    setLogLevel(sc, "WARN")

    print ('Session:', spark)
    print ('SparkContext', sc)

    # Create DataFrame representing the stream of input lines from connection to host:port
    lines = spark\
        .readStream\
        .format('socket')\
        .option('host', host)\
        .option('port', port)\
        .load()

    # Define schema for the incoming data
    schema = StructType([
        StructField("datetime", TimestampType(), True),
        StructField("open", FloatType(), True),
        StructField("high", FloatType(), True),
        StructField("low", FloatType(), True),
        StructField("close", FloatType(), True),
        StructField("volume", FloatType(), True),
        StructField("symbol", StringType(), True)
    ])
    # Parse the JSON data
    parsed = lines.select(from_json(col("value"), schema).alias("data")).select("data.*")

    aaplPrice = parsed.filter(col("symbol") == "AAPL")
    msftPrice = parsed.filter(col("symbol") == "MSFT")

    # Generate windows
    aapl10Day = aaplPrice.groupBy(window(col("datetime"), "10 days"), col("symbol")).agg(avg(col("close")).alias("aapl10DayMA")).select("aapl10DayMA", "window.end")
    aapl40Day = aaplPrice.groupBy(window(col("datetime"), "40 days"), col("symbol")).agg(avg(col("close")).alias("aapl40DayMA")).select("aapl40DayMA", "window.end")
    msft10Day = msftPrice.groupBy(window(col("datetime"), "10 days"), col("symbol")).agg(avg(col("close")).alias("msft10DayMA")).select("msft10DayMA", "window.end")
    msft40Day = msftPrice.groupBy(window(col("datetime"), "40 days"), col("symbol")).agg(avg(col("close")).alias("msft40DayMA")).select("msft40DayMA", "window.end")

    # Compare two moving averages to indicate buy/sell signals
    aaplMA = aapl10Day.join(aapl40Day, "end")
    aaplSignals = aaplMA.withColumn("signal", when(col("aapl10DayMA") > col("aapl40DayMA"), "buy").otherwise("sell"))
    msftMA = msft10Day.join(msft40Day, "end")
    msftSignals = msftMA.withColumn("signal", when(col("msft10DayMA") > col("msft40DayMA"), "buy").otherwise("sell"))

    signals = aaplSignals.select("end", lit("AAPL").alias("symbol"), "signal").union(msftSignals.select("end", lit("MSFT").alias("symbol"), "signal"))
    
    query = signals\
        .writeStream\
        .outputMode('append')\
        .format('console')\
        .start()

    query.awaitTermination()

    # ../Python-3.9.2/bin/spark-submit