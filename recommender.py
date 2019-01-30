# Import libraries
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


# Import textfile from location into RDD variables 
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

    
    
    # Print average score of the model for all users for the specified rank
    # YOUR CODE GOES HERE
    
    
rankList = [2,10,20]
for rank in rankList:
    model = ALS.trainImplicit(trainData, rank , seed=345)
    modelEval(model,validationData)
    
    
    
bestModel = ALS.trainImplicit(trainData, rank=10, seed=345)
modelEval(bestModel, testData) 


# Find the top 5 artists for a particular user and list their names
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
