from flask import Flask, request, render_template, jsonify
import pandas as pd
import re
import csv
import os

import model
app = Flask(__name__, static_folder='static', static_url_path='/static')

# Load song dataset
df = pd.read_csv('data/dataset.csv')

def normalize(text):
    return re.sub(r"[^\w\s]", "", text.lower())

df['track_name_normalized'] = df['track_name'].fillna('').apply(normalize)
df['artists_normalized'] = df['artists'].fillna('').apply(normalize)

# Store favorites in memory
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
    "world-music": "#32CD32"
}



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search_track():
    query = normalize(request.args.get('q', ''))

    if not query or len(query) < 2:
        return ""

    track_matches = df['track_name_normalized'].str.contains(query, na=False)
    artist_matches = df['artists_normalized'].str.contains(query, na=False)

    results = df[track_matches | artist_matches].head(6)

    return  (
        ''.join(
        f"""
        <div style="border:2px solid {genre_colors[row['track_genre']]} !important" class='p-2 border rounded-xl  flex justify-between items-center'>
            <span>{row['track_name']} - {row['artists']}</span>
            <span>Genre: {row['track_genre']}</span>

            <form 
                data-favorite
                data-track="{row['track_name']}" 
                data-artist="{row['artists']}">
                <button 
                    type="submit"
                    class='ml-4   px-2 py-1 rounded favBtn'>
                    ★
                </button>
            </form>
        </div>
        """
        for _, row in results.iterrows()
    )
    )

@app.route('/add_favorite', methods=['POST'])
def add_favorite():
    track = request.form.get('track')
    artist = request.form.get('artist')

    if not track or not artist:
        return "Missing data", 400

    # Avoid duplicates
    if any(fav['track'] == track and fav['artist'] == artist for fav in FAVORITES):
        return "Already added", 200

    FAVORITES.append({'track': track, 'artist': artist})

    # Overwrite the CSV with current list
    with open('data/favorites.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['track', 'artist'])
        writer.writeheader()
        writer.writerows(FAVORITES)

    return "Added", 200

if __name__ == '__main__':
    app.run(debug=True)
