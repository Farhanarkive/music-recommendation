import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

df = pd.read_csv('musicboard_ratings_cleaned.csv')

user_item_matrix = df.pivot_table(index='User', columns='Album', values='Rating')

# fill NaNs with 0 
user_item_matrix_filled = user_item_matrix.fillna(0)

# collaborative filtering

# compute cosine similarity between users
user_similarity = cosine_similarity(user_item_matrix_filled)

user_similarity_df = pd.DataFrame(user_similarity, index=user_item_matrix.index, columns=user_item_matrix.index)

def recommend_collaborative(user_id, n_recommendations=5):
    similar_users = user_similarity_df[user_id].sort_values(ascending=False).index[1:]  # skip self
    similar_user_ratings = user_item_matrix.loc[similar_users]
    
    # weighted average of similar users ratings
    recommendation_scores = similar_user_ratings.mean(axis=0)
    
    # remove albums the user has already rated
    rated_albums = user_item_matrix.loc[user_id].dropna().index
    recommendation_scores = recommendation_scores.drop(rated_albums, errors='ignore')
    
    top_recommendations = recommendation_scores.sort_values(ascending=False).head(n_recommendations)
    return top_recommendations

# content based filtering

album_mean_ratings = df.groupby('Album')['Rating'].mean()

def recommend_content(user_id, n_recommendations=5):
    rated_albums = user_item_matrix.loc[user_id].dropna().index
    unrated_albums = album_mean_ratings.drop(rated_albums, errors='ignore')
    top_recommendations = unrated_albums.sort_values(ascending=False).head(n_recommendations)
    return top_recommendations


user_to_recommend = df['User'].iloc[0]  # pick any user ID from the dataset

print("\nCollaborative Filtering Recommendations:")
print(recommend_collaborative(user_to_recommend))

print("\nContent-Based Filtering Recommendations:")
print(recommend_content(user_to_recommend))
