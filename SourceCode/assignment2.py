from pyspark.ml.feature import VectorAssembler
from pyspark.ml.clustering import KMeans
from pyspark.ml.evaluation import ClusteringEvaluator
from pyspark.ml.feature import StandardScaler
from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession

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

#We are trying to find the optimal number of Clusters.
#So we will try 10 different numbers of clusters for each initialization methods of k-means:Random and K-means||.

for i in ['random','k-means||']:
	silhouette_score=list()
	silscoreandCls=list()
	for j in range(2,12):
		#Inserting Kmeans, and creating our model
		KMeans_algorithm=KMeans(featuresCol='standardized', k=j,initMode=i)
		model=KMeans_algorithm.fit(data_scale_output)
		output=model.transform(data_scale_output)

		#Printing each cluster's centers
		clcenters = model.clusterCenters()
		print("Cluster Centers are: ")
		for center in clcenters:
			print(center)
		#Computing and printing Sillhouette Score
		score=evaluator.evaluate(output)
		silhouette_score.append(score)
		print("Silhouette Score:",score)
		#Computing The Summary of Squared Errors and the Cluster Sizes
		sse=model.summary.trainingCost
		clustersizes=model.summary.clusterSizes
		silscoreandCls.append([score,j,clustersizes,i])
		print("For "+ str(j) +" clusters and centers initialized by " +i +" the Summary of Squared Errors is: "+str(sse)+" and the Cluster Sizes are: "+str(clustersizes))
	maxsil=max(silhouette_score)
	maxsilandK=silhouette_score.index(maxsil)
	print("The Clusters are "+str(silscoreandCls[maxsilandK][1])+" , Sillhouette Score is: "+str(maxsil)+" and cluster sizes are: "+str(silscoreandCls[maxsilandK][2])+" with "+str(silscoreandCls[maxsilandK][3])+" initialization.")
