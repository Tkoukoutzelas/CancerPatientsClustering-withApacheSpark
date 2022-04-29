from pyspark.ml.feature import VectorAssembler
from pyspark.ml.clustering import KMeans
from pyspark.ml.evaluation import ClusteringEvaluator
from pyspark.ml.feature import StandardScaler
from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession
import sys

#User defined arguments for number of clusters and centers initialization method
i,init=int(sys.argv[1]),sys.argv[2]
if init=='k-means':
    init=init+'||'
    
#Creating Spark Session    
sc = SparkContext.getOrCreate()
spark = SparkSession(sc)

#Importing the patients data from Hadoop's DFS and dropping possible null values.
pat_data=spark.read.csv("hdfs://master:9000/user/user/input/meddata2022.csv", header=False, inferSchema=True)
pat_data = pat_data.na.drop()

#Our data gets entered in a feature vector
assemble=VectorAssembler(inputCols=['_c0','_c1','_c2','_c3','_c4'],outputCol='features')
assembled_data=assemble.transform(pat_data)

#The data scales may vary, so we perform a Standardization on it
scale=StandardScaler(inputCol='features',outputCol='standardized')
data_scale=scale.fit(assembled_data)
data_scale_output=data_scale.transform(assembled_data)

#Creating an Evaluator so we can later compute the Sillhouette Score for each cluster number
evaluator = ClusteringEvaluator(predictionCol='prediction',featuresCol='standardized', metricName='silhouette', distanceMeasure='squaredEuclidean')

#Inserting Kmeans, and creating our model
KMeans_algorithm=KMeans(featuresCol='standardized', k=i,initMode=init)
model=KMeans_algorithm.fit(data_scale_output)
output=model.transform(data_scale_output)
#Printing each cluster's centers
clcenters = model.clusterCenters()
print("Cluster Centers are: ")
for center in clcenters:
    print(center)
    
#Computing and printing Sillhouette Score
score=evaluator.evaluate(output)
print("Silhouette Score for 6 Clusters:",score)
#Computing and printing The Summary of Squared Errors
sse=model.summary.trainingCost
print("The Sum of Squared Errors for 6 Clusters is:"+str(sse))
