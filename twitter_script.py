#!/usr/bin/python3

# Import modules
import tweepy
import json
from geopy import geocoders
import time
import csv

gn = geocoders.GeoNames(username='')

coordinates_arr = []
csvdata = []

bearer_token = ""
auth = tweepy.OAuth2BearerHandler(bearer_token)
api = tweepy.API(auth)

trend_locations = api.available_trends()

# Get trending topics worldwide
woeid = 1
trends = api.get_place_trends(woeid)

#Get the amount of trending topics
trend_amount = len(trends[0]['trends'])
print("Amount of trending topics: ", trend_amount)

for trend in trends[0]['trends']:
    print( "Trend: " , trend['name'])
    pages = tweepy.Cursor(api.search_tweets, q=trend['name'], 
                    tweet_mode='extended',count=100).pages()
    #only loop through the first 7 pages -> Limit Rate problems
    for i in range(7):
        try:
            tweets = next(pages)
        except tweepy.TweepyException:
            print("no more pages....")
            break
        except StopIteration:
            break

        print("Anzal Tweets in page: ", len(tweets))
        for tweet in tweets:
            if tweet._json['place'] is not None:
                # Get coordinates from tweet
                gc = gn.geocode(tweet._json['place']['full_name'])
                if gc is not None:
                    coordinates_arr.append([gc.latitude, gc.longitude])
                    csvdata.append(["02/12/2022", gc.latitude, gc.longitude, 10,trend['name']])
                    coordinates = tweet._json['place']['bounding_box']['coordinates'][0][0]
                    print(tweet._json['place']['full_name'],': ',coordinates)  

#export csv
header = ['Date','Latitude','Longitude','Depth','Type']
with open('twitter-trending-topics-clustering.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(csvdata)

#print amount of elements in corrdinates array
print( "Amount of elements in coordinates array: " , len(coordinates_arr))
## K-Means Clustering
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np

# Convert to numpy array
coordinates_arr = np.array(coordinates_arr)

# ellbow method to find optimal k
distortions = []
K = range(2,12)
for k in K:
    kmeanModel = KMeans(n_clusters=k)
    kmeanModel.fit(coordinates_arr)
    distortions.append(kmeanModel.inertia_)

plt.figure(figsize=(16,8))
plt.plot(K, distortions, 'bx-')
plt.xlabel('k')
plt.ylabel('Distortion')
plt.title('The Elbow Method showing the optimal k')
plt.show()


# Create K-Means model
var = input("Enter cluster size")
clusterSize = int(var)
#kmeans = KMeans(n_clusters=3, random_state=0).fit(coordinates_arr)
kmeans = KMeans(n_clusters=clusterSize, random_state=0).fit(coordinates_arr)

# Get cluster centers
centers = kmeans.cluster_centers_

# Plot clusters
plt.scatter(coordinates_arr[:,0], coordinates_arr[:,1], c=kmeans.labels_.astype(float), s=50, alpha=0.5)
plt.scatter(centers[:, 0], centers[:, 1], c='red', s=50)
plt.show()