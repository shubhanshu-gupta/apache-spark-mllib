"""Movie lens data prediction"""

import sys

from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.recommendation import ALS
from pyspark.sql import Row

spark = SparkSession\
        .builder\
        .appName("ALSExample")\
        .getOrCreate()

lines = spark.read.text("/home/shubhanshu/Documents/spark-2.0.0-bin-hadoop2.7/data/mllib/als/sample_movielens_ratings.txt").rdd

parts = lines.map(lambda row: row.value.split("::"))
ratingsRDD = parts.map(lambda p: Row(userId=int(p[0]), movieId=int(p[1]),
									 rating=float(p[2]), timestamp=long(p[3])))
ratings = spark.createDataFrame(ratingsRDD)

ratings.show()
# print len(ratings.userId)