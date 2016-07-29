"""Letter counting script"""

from pyspark import SparkContext

logFile = "/home/shubhanshu/Documents/spark-2.0.0-bin-hadoop2.7/README.md"
sc = SparkContext("local", "Simple App")
logData = sc.textFile(logFile).cache()

#We are counting the number of a and b alphabets present in the text file
numAs = logData.filter(lambda s: 'a' in s).count()
numBs = logData.filter(lambda s: 'b' in s).count()

print("Lines with a: %i, lines with b: %i" % (numAs, numBs))

sc.stop()