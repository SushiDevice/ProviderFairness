import pandas as pd

# Cargar los archivos del dataset AMBAR
artists = pd.read_csv("artists_info.csv")
ratings = pd.read_csv("ratings_info.csv")
tracks = pd.read_csv("tracks_info.csv")
users = pd.read_csv("users_info.csv")

# Combinar ratings con tracks
merged = pd.merge(ratings, tracks, on="track_id", how="inner")

# Agregar información de continente desde artists
merged = pd.merge(merged, artists[["artist_id", "continent"]], on="artist_id", how="inner")

# Seleccionar columnas necesarias para train_set.csv
train_set = merged[["user_id", "track_id", "rating", "continent", "styles"]]
train_set.columns = ["user", "track_id", "rating", "continent", "genre"]

# Agregar una columna de ID auto-incremental
train_set.insert(0, 'id', range(1, len(train_set) + 1))

# Guardar el archivo
train_set.to_csv("for_testing.csv", index=False)