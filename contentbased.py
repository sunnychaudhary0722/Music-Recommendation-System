import numpy as np
import pandas as pd
# Import LabelEncoder
from sklearn import preprocessing
from sklearn.cluster import KMeans
import pickle



dataset = pd.read_csv("songsData.csv")
dataset.dropna(inplace=True)
dataset.drop_duplicates(subset='song_name', keep='first', inplace=True)
features = dataset.iloc[:, :-1]
song_names = dataset.iloc[:, -1].values

# Creating labelEncoder
le = preprocessing.LabelEncoder()
# Converting string labels into numbers.
features['genre'] = le.fit_transform(features['genre'])

# giving k =1500
kmeans = KMeans(1500)
kmeans.fit(features)
labels = kmeans.labels_
dataset['labels'] = labels
dict1 = {}
for i in range(0, 15436):
   if labels[i] not in dict1.keys():
      dict1[labels[i]] = []
   dict1[labels[i]].append(song_names[i])

dict2={}
for i in range(0,15436):
    dict2[song_names[i]]=labels[i]

pickle.dump(dict1, open('dict1.pkl', 'wb'))
pickle.dump(dict2, open('dict2.pkl', 'wb'))
