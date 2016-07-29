"""Movie lens data prediction"""

import sys

from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.recommendation import ALS
from pyspark.sql import Row
from numpy import array

spark = SparkSession\
        .builder\
        .appName("ALSExample")\
        .getOrCreate()

lines = spark.read.text("/home/shubhanshu/Documents/spark-2.0.0-bin-hadoop2.7/data/mllib/als/sample_movielens_ratings.txt").rdd

parts = lines.map(lambda row: row.value.split("::"))
ratingsRDD = parts.map(lambda p: Row(userId=int(p[0]), movieId=int(p[1]),
									 rating=float(p[2]), timestamp=long(p[3])))
ratings = spark.createDataFrame(ratingsRDD)

(training, test) = ratings.randomSplit([0.8, 0.2])

als = ALS(maxIter=5, regParam=0.01, userCol="userId", itemCol="movieId", ratingCol="rating")
model = als.fit(training)

predictions = model.transform(test)
evaluator = RegressionEvaluator(metricName="rmse", labelCol="rating", predictionCol="prediction")

rmse = evaluator.evaluate(predictions)
print "Root-mean-square error = " + str(rmse)
spark.stop()

##### Tried working with test.data, but didn't work out. Need to study more ########
# sc = SparkContext("local", "ALSApp")
# data = sc.textFile("/home/shubhanshu/Documents/spark-2.0.0-bin-hadoop2.7/data/mllib/als/test.data")
# test_ratings = data.map(lambda line: array([float(x) for x in line.split(',')]))

# model = ALS(test_ratings, 1, 20)

# testdata = ratings.map(lambda p: (int(p[0]), int(p[1])))
# test_predictions = model.predictAll(testdata).map(lambda r: ((r[0], r[1]), r[2]))
# ratesAndPreds = test_ratings.map(lambda r: ((r[0], r[1]), r[2])).join(test_predictions)
# MSE = ratesAndPreds.map(lambda r: (r[1][0] - r[1][1])**2).reduce(lambda x, y: x + y)/ratesAndPreds.count()

# print "Mean Squared Error = " + str(MSE)

#ratings.show()
# https://spark.apache.org/docs/0.9.2/mllib-guide.html#collaborative-filtering-2