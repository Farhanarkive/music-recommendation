import pandas as pd

df = pd.read_csv('musicboard_ratings.csv')

# before cleaning
print(f"Original rows: {len(df)}")

# drop duplicate ratings
# keep only the first rating if a user rated the same album multiple times
df_cleaned = df.drop_duplicates(subset=['User', 'Album'])

# after cleaning
print(f"Rows after cleaning: {len(df_cleaned)}")
print(f"Unique users: {len(df_cleaned['User'].unique())}")
print(f"Unique albums: {len(df_cleaned['Album'].unique())}")

# save cleaned data
df_cleaned.to_csv('musicboard_ratings_cleaned.csv', index=False)


