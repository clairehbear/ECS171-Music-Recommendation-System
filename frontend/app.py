from flask import Flask, request, render_template, jsonify
import pandas as pd
import re
import csv
import os
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler

app = Flask(__name__, static_folder="static", static_url_path="/static")

# Load song dataset
df = pd.read_csv("data/dataset.csv")
# Remove duplicates based on track name and artist
df = df.drop_duplicates(subset=["track_name", "artists"], keep="first")
df = df.reset_index(drop=True)  # Reset index after removing duplicates

# Load cosine similarity model
with open("../backend/models/cos.pkl", "rb") as file:
    cos_model = pickle.load(file)

# Standardize data for recommendations
scaler = StandardScaler()
features = [
    "popularity",
    "danceability",
    "loudness",
    "acousticness",
    "valence",
    "tempo",
]
X_scaled = scaler.fit_transform(df[features])
cos_scaled = X_scaled / np.linalg.norm(X_scaled, axis=1)[:, np.newaxis]


def normalize(text):
    return re.sub(r"[^\w\s]", "", text.lower())


df["track_name_normalized"] = df["track_name"].fillna("").apply(normalize)
df["artists_normalized"] = df["artists"].fillna("").apply(normalize)

# If exists, load favorites from CSV
FAVORITES = []
genre_colors = {
    "acoustic": "#4E8C8A",
    "afrobeat": "#FF7F00",
    "alt-rock": "#7E7EB8",
    "alternative": "#8A8ACB",
    "ambient": "#5D8AA8",
    "anime": "#FF6B6B",
    "black-metal": "#222222",
    "bluegrass": "#3A5F0B",
    "blues": "#1A5F9E",
    "brazil": "#009C3B",
    "breakbeat": "#FF4500",
    "british": "#C8102E",
    "cantopop": "#E60026",
    "chicago-house": "#00A1E0",
    "children": "#FFD700",
    "chill": "#87CEEB",
    "classical": "#D4AF37",
    "club": "#9400D3",
    "comedy": "#FFA500",
    "country": "#8B4513",
    "dance": "#FF00FF",
    "dancehall": "#FF8C00",
    "death-metal": "#8B0000",
    "deep-house": "#1E90FF",
    "detroit-techno": "#4169E1",
    "disco": "#9370DB",
    "disney": "#00BFFF",
    "drum-and-bass": "#32CD32",
    "dub": "#FFD700",
    "dubstep": "#00FF7F",
    "edm": "#FF1493",
    "electro": "#00FFFF",
    "electronic": "#7B68EE",
    "emo": "#800080",
    "folk": "#556B2F",
    "forro": "#2E8B57",
    "french": "#0055A4",
    "funk": "#FFA500",
    "garage": "#FF6347",
    "german": "#000000",
    "gospel": "#FFD700",
    "goth": "#708090",
    "grindcore": "#8B0000",
    "groove": "#20B2AA",
    "grunge": "#696969",
    "guitar": "#DC143C",
    "happy": "#FFD700",
    "hard-rock": "#B22222",
    "hardcore": "#FF0000",
    "hardstyle": "#FF4500",
    "heavy-metal": "#B8860B",
    "hip-hop": "#FF8C00",
    "honky-tonk": "#CD853F",
    "house": "#1E90FF",
    "idm": "#9932CC",
    "indian": "#FF9933",
    "indie-pop": "#FF69B4",
    "indie": "#DA70D6",
    "industrial": "#A9A9A9",
    "iranian": "#10C829",
    "j-dance": "#FF6B6B",
    "j-idol": "#FFB6C1",
    "j-pop": "#FF69B4",
    "j-rock": "#E32636",
    "jazz": "#D2691E",
    "k-pop": "#FF0000",
    "kids": "#FFD700",
    "latin": "#FF8C00",
    "latino": "#FF4500",
    "malay": "#FF6347",
    "mandopop": "#E60026",
    "metal": "#808080",
    "metalcore": "#8B008B",
    "minimal-techno": "#00BFFF",
    "mpb": "#2E8B57",
    "new-age": "#AFEEEE",
    "opera": "#DAA520",
    "pagode": "#FF6347",
    "party": "#FF00FF",
    "piano": "#D2B48C",
    "pop-film": "#FFA07A",
    "pop": "#FF69B4",
    "power-pop": "#FF6347",
    "progressive-house": "#00CED1",
    "psych-rock": "#9370DB",
    "punk-rock": "#FF0000",
    "punk": "#FF4500",
    "r-n-b": "#4169E1",
    "reggae": "#FFD700",
    "reggaeton": "#9AC77F",
    "rock-n-roll": "#FF0000",
    "rock": "#B22222",
    "rockabilly": "#CD5C5C",
    "romance": "#FF69B4",
    "sad": "#1E90FF",
    "salsa": "#FF4500",
    "samba": "#FF8C00",
    "sertanejo": "#2E8B57",
    "show-tunes": "#DAA520",
    "singer-songwriter": "#8FBC8F",
    "ska": "#00FF7F",
    "sleep": "#4169E1",
    "songwriter": "#8FBC8F",
    "soul": "#FF8C00",
    "spanish": "#FF0000",
    "study": "#4682B4",
    "swedish": "#0055A4",
    "synth-pop": "#9370DB",
    "tango": "#8B0000",
    "techno": "#00FFFF",
    "trance": "#7B68EE",
    "trip-hop": "#9932CC",
    "turkish": "#E30A17",
    "world-music": "#32CD32",
}


FAVORITES_FILE = "data/favorites.csv"
if os.path.exists(FAVORITES_FILE):
    with open(FAVORITES_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        FAVORITES = list(reader)


@app.route("/")
def index():
    return render_template("index.html", favorites=FAVORITES)


@app.route("/search", methods=["GET"])
def search_track():
    query = normalize(request.args.get("q", ""))

    if not query or len(query) < 2:
        return ""

    track_matches = df["track_name_normalized"].str.contains(query, na=False)
    artist_matches = df["artists_normalized"].str.contains(query, na=False)

    results = df[track_matches | artist_matches].head(10)

    return "".join(
        f"""
        <div style="border:2px solid {genre_colors[row['track_genre']]} !important" class='p-2 border rounded-xl  flex justify-between items-center'>
            <span>{row['track_name']} - {row['artists']}</span>
            <div class="flex items-center gap-4">
                <span class="bg-gray-200 text-gray-700 px-2 py-1 rounded text-sm">{row['track_genre']}</span>

                <form 
                    data-favorite
                    data-track="{row['track_name']}" 
                    data-artist="{row['artists']}">
                    <button 
                        type="submit"
                        class='px-2 py-1 rounded favBtn'>
                        ★
                    </button>
                </form>
            </div>
        </div>
        """
        for _, row in results.iterrows()
    )


@app.route("/add_favorite", methods=["POST"])
def add_favorite():
    track = request.form.get("track")
    artist = request.form.get("artist")

    if not track or not artist:
        return "Missing data", 400

    if any(fav["track"] == track and fav["artist"] == artist for fav in FAVORITES):
        return "Already added", 200

    FAVORITES.append({"track": track, "artist": artist})

    with open(FAVORITES_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["track", "artist"])
        writer.writeheader()
        writer.writerows(FAVORITES)

    return "Added", 200


@app.route("/remove_favorite", methods=["POST"])
def remove_favorite():
    track = request.form.get("track")
    artist = request.form.get("artist")

    global FAVORITES
    FAVORITES = [
        fav
        for fav in FAVORITES
        if not (fav["track"] == track and fav["artist"] == artist)
    ]

    with open(FAVORITES_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["track", "artist"])
        writer.writeheader()
        writer.writerows(FAVORITES)

    return "Removed", 200


@app.route("/clear_favorites", methods=["POST"])
def clear_favorites():
    global FAVORITES
    FAVORITES = []

    with open(FAVORITES_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["track", "artist"])
        writer.writeheader()

    return "Cleared", 200


@app.route("/get_recommendations", methods=["POST"])
def get_recommendations():
    if not FAVORITES:
        return """
        <div class="text-gray-400 italic text-center p-4">
            Add some songs to your favorites and click "Get My Song Recommendations" to discover new music!
        </div>
        """

    # Get indices of favorite songs
    playlist_indices = []
    for fav in FAVORITES:
        matches = df[
            (df["track_name"] == fav["track"]) & (df["artists"] == fav["artist"])
        ]
        if not matches.empty:
            playlist_indices.append(matches.index[0])

    if not playlist_indices:
        return """
        <div class="text-gray-400 italic text-center p-4">
            Could not find your favorite songs in the database. Try adding different songs.
        </div>
        """

    # Get clusters for favorite songs
    playlist_clusters = cos_model.predict(cos_scaled[playlist_indices])
    majority_cluster = np.argmax(np.bincount(playlist_clusters))

    # Get indices of songs in same cluster
    cluster_indices = df.index[cos_model.predict(cos_scaled) == majority_cluster]

    # Compute correlation scores for each song in cluster
    song_scores = []
    for song_idx in cluster_indices:
        score = float("inf")
        for liked_song_idx in playlist_indices:
            correlation = np.corrcoef(cos_scaled[song_idx], cos_scaled[liked_song_idx])[
                0, 1
            ]
            score = min(score, 1 - correlation)  # Convert correlation to distance
        song_scores.append(score)

    # top 10 recommendations
    top_k = 10
    song_scores = np.array(song_scores)
    # include more songs
    most_similar = np.argsort(song_scores)[len(FAVORITES):len(FAVORITES) + top_k]
    recommended_indices = cluster_indices[most_similar]
    recommended_songs = df.iloc[recommended_indices]

    # exclude songs already in favorites
    favorite_set = set((fav["track"], fav["artist"]) for fav in FAVORITES)
    filtered_songs = recommended_songs[
        ~recommended_songs.apply(
            lambda row: (row["track_name"], row["artists"]) in favorite_set, axis=1
        )
    ]
    filtered_songs = filtered_songs.head(top_k)

    recommendations_html = ""
    for _, song in filtered_songs.iterrows():
        recommendations_html += f"""
        <div style="border:2px solid {genre_colors[song['track_genre']]} !important" class='p-2 border rounded-xl flex justify-between items-center'>
            <span>{song['track_name']} - {song['artists']}</span>
            <span class="bg-gray-200 text-gray-700 px-2 py-1 rounded text-sm">{song['track_genre']}</span>

             <form 
                    data-favorite
                    data-track="{song['track_name']}" 
                    data-artist="{song['artists']}">
                    <button 
                        type="submit"
                        class='px-2 py-1 rounded favBtn'>
                        ★
                    </button>
                </form>
        </div>
        """

    return recommendations_html


if __name__ == "__main__":
    app.run(debug=True)
