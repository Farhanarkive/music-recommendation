import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
import json
import time

album_ids = list(range(247717244, 247717244 + 100))

all_data = []

for album_id in album_ids:
    print(f"Scraping album {album_id}...")
    url = f"https://api.musicboard.app/v2/ratings/?content_id={album_id}&content_type=album"
    offset = 0
    response = requests.get(url)
    results = json.loads(response.text)

    if 'results' not in results:  # in case album id is invalid
        print(f"Album {album_id} had no results, skipping.")
        continue

    while (offset < results['count']):
        for entry in results['results']:
            if entry['rating']:
                all_data.append({
                    'User': entry['creator']['uid'],
                    'Album': album_id,
                    'Rating': entry['rating'],
                    'Timestamp': entry['created_at']
                })
        offset += 24
        if results['next']:
            response = requests.get(results['next'])
            results = json.loads(response.text)
        else:
            break
    time.sleep(0.2)  

df = pd.DataFrame(all_data)

df.to_csv('musicboard_ratings.csv', index=False)

print(f"Total Ratings Collected: {len(df)}")
print(f"Unique Users: {len(pd.unique(df['User']))}")
print(f"Unique Albums: {len(pd.unique(df['Album']))}")

