from flask import Flask, request, render_template
import re
import pandas as pd

app = Flask(__name__)
df = pd.read_csv('data/dataset.csv')

@app.route('/')
def index():
    return render_template('index.html')

def normalize(text):
    # remove punctuation and make words lowercase
    return re.sub(r"[^\w\s]", "", text.lower())

@app.route('/search', methods=['GET'])
def search_track():
    query = normalize(request.args.get('q', ''))

    # apply normalization
    df['track_name_normalized'] = df['track_name'].fillna('').apply(normalize)
    df['artists_normalized'] = df['artists'].fillna('').apply(normalize)

    track_matches = df['track_name_normalized'].str.contains(query, na=False)
    artist_matches = df['artists_normalized'].str.contains(query, na=False)

    results = df[track_matches | artist_matches].head(6)

    html = ''.join(
                    f"<div class='p-2 border rounded bg-gray-50'>{row['track_name']} - {row['artists']}</div>"
                    for _, row in results.iterrows())
    
    return html

if __name__ == '__main__':
    app.run(debug=True)
