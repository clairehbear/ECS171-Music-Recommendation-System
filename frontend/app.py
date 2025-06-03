from flask import Flask, request, render_template, jsonify
import pandas as pd
import re
import csv
import os

app = Flask(__name__)

# Load song dataset
df = pd.read_csv('data/dataset.csv')

def normalize(text):
    return re.sub(r"[^\w\s]", "", text.lower())

df['track_name_normalized'] = df['track_name'].fillna('').apply(normalize)
df['artists_normalized'] = df['artists'].fillna('').apply(normalize)

# Store favorites in memory
FAVORITES = []

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

    html = ''.join(
        f"""
        <div class='p-2 border rounded-xl bg-green-800 flex justify-between items-center'>
            <span>{row['track_name']} - {row['artists']}</span>
            <form 
                data-favorite
                data-track="{row['track_name']}" 
                data-artist="{row['artists']}">
                <button 
                    type="submit"
                    class='ml-4 text-sm bg-green-600 px-2 py-1 rounded'>
                    Add to Favorites
                </button>
            </form>
        </div>
        """
        for _, row in results.iterrows()
    )
    return html

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
