import pandas as pd
import numpy as np

# Read the data files
print("Reading data files...")
users_df = pd.read_csv('data/AMBAR/users_info.csv')
artists_df = pd.read_csv('data/AMBAR/artists_info.csv')
ratings_df = pd.read_csv('data/AMBAR/ratings_info.csv')

# Clean and prepare user data
print("Preparing user data...")
users_df['continent'] = users_df['continent'].fillna('Unknown')

# Clean and prepare artist data
print("Preparing artist data...")
# Split the category_styles into primary genre
artists_df['primary_genre'] = artists_df['category_styles'].str.split('|').str[0]

# Merge data
print("Merging data...")
# First merge ratings with users
merged_df = pd.merge(ratings_df, users_df[['user_id', 'continent']], 
                    left_on='user_id', right_on='user_id', how='left')

# Then merge with artists
merged_df = pd.merge(merged_df, artists_df[['artist_id', 'primary_genre']], 
                    left_on='artist_id', right_on='artist_id', how='left')

# Prepare final format
print("Preparing final format...")
final_df = pd.DataFrame({
    'user': merged_df['user_id'],
    'continent': merged_df['continent'],
    'genre': merged_df['primary_genre'],
    'rating': merged_df['rating']
})

# Remove any rows with missing values
final_df = final_df.dropna()

# Save the formatted data
print("Saving formatted data...")
final_df.to_csv('for_testing.csv', index=False)

print("Conversion complete! Data saved to for_testing.csv") 