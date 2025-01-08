import pandas as pd
from pathlib import Path

# Set up paths
data_dir = Path('data/AMBAR')
output_dir = Path('data')

# Read the CSV files
ratings_df = pd.read_csv(data_dir / 'ratings_info.csv')
artists_df = pd.read_csv(data_dir / 'artists_info.csv')
tracks_df = pd.read_csv(data_dir / 'tracks_info.csv')
users_df = pd.read_csv(data_dir / 'users_info.csv')

# Print column names to debug
print("Ratings columns:", ratings_df.columns.tolist())
print("Artists columns:", artists_df.columns.tolist())
print("Tracks columns:", tracks_df.columns.tolist())
print("Users columns:", users_df.columns.tolist())

# Merge the dataframes to get all required information
# First merge tracks with artists to get genre (styles) and continent
tracks_with_artists = pd.merge(
    tracks_df,
    artists_df[['artist_id', 'continent', 'category_styles']],
    on='artist_id',
    how='left',
    suffixes=('_track', '_artist')
)

print("Tracks with artists columns:", tracks_with_artists.columns.tolist())

# Then merge with ratings
merged_df = pd.merge(
    ratings_df,
    tracks_with_artists[['track_id', 'continent', 'category_styles_artist']],
    on='track_id',
    how='left'
)

# Finally merge with users to get user continent
final_df = pd.merge(
    merged_df,
    users_df[['user_id', 'continent']],
    on='user_id',
    how='left',
    suffixes=('_artist', '_user')
)

# Rename columns to match MOReGIn requirements
moregin_df = final_df.rename(columns={
    'user_id': 'user',
    'track_id': 'item',
    'category_styles_artist': 'genre',
    'continent_artist': 'continent'
})

# Select and reorder columns as needed by MOReGIn
moregin_df = moregin_df[['user', 'item', 'rating', 'continent', 'genre']]

# Save the merged dataset
output_file = output_dir / 'for_testing.csv'
moregin_df.to_csv(output_file, index=False)

print(f"Created MOReGIn input file at: {output_file}")
print(f"Total records: {len(moregin_df)}") 