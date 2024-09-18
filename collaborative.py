import warnings
import pickle
import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from recommender import Recommender

warnings.filterwarnings("ignore")

# reading dataset
df_songs = pd.read_csv('songs.csv')

song_user = df_songs.groupby('user_id')['song_id'].count()
# Get users which have listen to at least 16 songs
song_ten_id = song_user[song_user > 16].index.to_list()
# Filtered the dataset to keep only those users with more than 16 listened
df_song_id_more_ten = df_songs[df_songs['user_id'].isin(song_ten_id)].reset_index(drop=True)

# convert the dataframe into a pivot table & for the songs users have not listened fillna is used to put 0 there
df_songs_features = df_song_id_more_ten.pivot(index='song_id', columns='user_id', values='listen_count').fillna(0)

# obtain a sparse matrix
mat_songs_features = csr_matrix(df_songs_features.values)

df_unique_songs = df_songs.drop_duplicates(subset=['song_id']).reset_index(drop=True)[['song_id', 'title']]
decode_id_song = {
    song: i for i, song in
    enumerate(list(df_unique_songs.set_index('song_id').loc[df_songs_features.index].title))
}

model = Recommender(metric='cosine', algorithm='brute', k=20, data=mat_songs_features,
                    decode_id_song=decode_id_song)
# song = 'I believe in miracles'

#new_recommendations = model.make_recommendation(new_song=song, n_recommendations=10)

pickle.dump(model, open('model.pkl', 'wb'))

