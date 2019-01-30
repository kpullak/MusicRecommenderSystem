# # Music Recommender System using Apache Spark and Python
# 
# ## Description
# 
# For this project, I created a recommender system that would recommend new musical artists to a user based on their listening history. Suggesting different songs or musical artists to a user is important to many music streaming services, such as Pandora and Spotify. In addition, this type of recommender system could also be used as a means of suggesting TV shows or movies to a user (e.g., Netflix). 
# 
# To create this system I used Spark and the collaborative filtering technique. 
# **Submission Instructions:** 
 
# ## Datasets
# 
# I have used publicly available song data from audioscrobbler, which can be found [here](http://www-etud.iro.umontreal.ca/~bergstrj/audioscrobbler_data.html). However, I modified the original data files so that the code would run in a reasonable time on a single machine.


# ## Necessary Package Imports

import findspark
findspark.init()

from pyspark.mllib.recommendation import *
import random
from operator import *
from collections import defaultdict


from pyspark import SparkContext, SparkConf
sc = SparkContext.getOrCreate()
sc.stop()
sc = SparkContext('local','Recommender')


# ## Loading data
# Loading the three datasets into RDDs and name them `artistData`, `artistAlias`, and `userArtistData`. 

artistData = sc.textFile("data_raw/artist_data_small.txt")
artistAlias = sc.textFile("data_raw/artist_alias_small.txt")
userArtistData = sc.textFile("data_raw/user_artist_data_small.txt")


# Split a sequence into seperate entities and store as int
userArtistDataNew = userArtistData.map(lambda line:line.split(" ")).map(lambda r: (int(r[0]), int(r[1]),int(r[2])))
artistAliasNew = artistAlias.map(lambda line:line.split("\t")).map(lambda r: (int(r[0]), int(r[1])))
artistDataNew = artistData.map(lambda line:line.split("\t")).map(lambda r: (int(r[0]), r[1]))

# Create a dictionary of the 'artistAlias' dataset
dict_art_alias = artistAliasNew.collectAsMap()

# If artistid exists, replace with artistsid from artistAlias, else retain original
dict_keys = list(dict_art_alias.keys())
userArtistDataCorrected = userArtistDataNew.map(lambda x:x if x[1] not in dict_keys else (x[0],dict_art_alias[x[1]],x[2]))

# Create an RDD consisting of 'userid' and 'playcount' objects of original tuple
temp_sum = userArtistDataCorrected.map(lambda r: (int(r[0]), int(r[2]))).reduceByKey(lambda a,b:a+b)

# Count instances by key and store in broadcast variable
temp_mean = userArtistDataCorrected.map(lambda r: (int(r[0]), int(r[1]))).groupByKey().map(lambda l:(l[0],len(list(l[1]))))

# Inorder to check if there is any difference between two rdds we can use subtract by key function
# print(mean.subtractByKey(userid_artistid_len_rdd).collect())

# Compute and display users with the highest playcount along with their mean playcount across artists
topThree = temp_sum.takeOrdered(3, key=lambda x: -x[1])
topThree1 = sc.parallelize(topThree)

a=topThree1.join(temp_mean).map(lambda x: (x[0],x[1][0],x[1][0]/x[1][1]))
my_list = a.collect()

from operator import itemgetter
temp_list = sorted(my_list, key=itemgetter(1))

for list_elems in reversed(temp_list):
    print("User "+str(int(list_elems[0]))+" has a total play count of "+str(int(list_elems[1]))+" and a mean play count of "+str(int(list_elems[2])))
    


# ####  Splitting Data for Testing
    
# Split the 'userArtistData' dataset into training, validation and test datasets. Store in cache for frequent access
trainData,validationData,testData=userArtistDataNew.randomSplit([0.4,0.4,0.2],13)

trainData.cache()
validationData.cache()
testData.cache()

# Display the first 3 records of each dataset followed by the total count of records for each datasets
print(trainData.take(3))
print(validationData.take(3))
print(testData.take(3))
print(trainData.count())
print(validationData.count())
print(testData.count())

# ## The Recommender Model
 
# ### Model Evaluation
# 
# Although there may be several ways to evaluate a model, I have used a simple method here. Suppose we have a model and some dataset of *true* artist plays for a set of users. This model can be used to predict the top X artist recommendations for a user and these recommendations can be compared the artists that the user actually listened to (here, X will be the number of artists in the dataset of *true* artist plays). Then, the fraction of overlap between the top X predictions of the model and the X artists that the user actually listened to can be calculated. This process can be repeated for all users and an average value returned.

# The function `modelEval` will take a model (the output of ALS.trainImplicit) and a dataset as input. Parameter Tuning is done one the validation data.After parameter tuning, the model can be evaluated on the test data.


def modelEval(model, dataset):
    
    # All artists in the 'userArtistData' dataset
    allArtists = userArtistDataCorrected.map(lambda x:x[1]).distinct()
    
    # Set of all users in the current (Validation/Testing) dataset
    valid_rdd = dataset.map(lambda x: ((x[0]),(x[1]))).groupByKey().map(lambda r: (int(r[0]), list(r[1]))).collectAsMap()
    users_list = list(valid_rdd.keys())
    
    # Create a dictionary of (key, values) for current (Validation/Testing) dataset
    # valid_rdd is created above
    
    # Create a dictionary of (key, values) for training dataset
    train_rdd = trainData.map(lambda x: ((x[0]),(x[1]))).groupByKey().map(lambda r: (int(r[0]), list(r[1]))).collectAsMap()
    
    # For each user, calculate the prediction score i.e. similarity between predicted and actual artists
    upon = 0
    for user in users_list:
        userPredict = []
        actualArtists = valid_rdd[user]
        ## NOTE: when using the model to predict the top-X artists for a user, do not include the artists listed with that user in the training data.
        artistExcTrain = set(allArtists.collect()) - set(train_rdd[user])
        # artistExcTrain = [x for x in allArtists.collect() if x not in train_rdd[user]]
        # The above method takes more time to work 
        # https://stackoverflow.com/questions/4211209/remove-all-the-elements-that-occur-in-one-list-from-another
        ## Creating a list with (user,artist) pairs
        for art in artistExcTrain:
            userPredict.append((user,art))
        # convert to an rdd
        userPredictRDD = sc.parallelize(userPredict)
        predictCount = model.predictAll(userPredictRDD)
        predictCountArtist = predictCount.map(lambda l: (l[1],l[2])).takeOrdered(len(actualArtists), key=lambda x: -x[1])
        # convert list to rdd
        predictCountArtistRDD = sc.parallelize(predictCountArtist)
        predictArtists = predictCountArtistRDD.map(lambda f:f[0]).collect()
        
        # score calculation
        a = list(set(predictArtists)&set(actualArtists)) 
        score = len(a)/float(len(predictArtists))
        upon = upon+score
    print(upon/float(len(users_list)))    

    
# ### Model Construction
    
rankList = [2,10,20]
for rank in rankList:
    model = ALS.trainImplicit(trainData, rank , seed=345)
    modelEval(model,validationData)
    
    
    
bestModel = ALS.trainImplicit(trainData, rank=10, seed=345)
modelEval(bestModel, testData) 



# ## Trying Some Artist Recommendations
# Using the best model above, predicting the top 5 artists for user `1059637` using the [recommendProducts](http://spark.apache.org/docs/1.5.2/api/python/pyspark.mllib.html#pyspark.mllib.recommendation.MatrixFactorizationModel.recommendProducts) function.

x = bestModel.recommendProducts(1059637,5)
recomendations = sc.parallelize(x)
recomendationArtists = recomendations.map(lambda r:r[1]).collect()
y = artistAliasNew.map(lambda x: ((x[0]),(x[1]))).groupByKey().map(lambda r: (int(r[0]), list(r[1]))).collect()
y_dict = dict((x[0], x[1]) for x in y)
realArt = artistDataNew.map(lambda x: ((x[0]),(x[1]))).groupByKey().map(lambda r: (int(r[0]), list(r[1]))).collect()
realArt_dict = dict((x[0], x[1]) for x in realArt)

i=0

for art in recomendationArtists:
    if art in realArt_dict.keys():
        i=i+1
        print ("Artist %d :"%i+ realArt_dict[art][0])
    else:
        alias=y_dict[art]
        i=i+1
        print ("Artist %d :"%i+ realArt_dict[alias][0])
