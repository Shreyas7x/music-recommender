from flask import Flask, render_template, request, jsonify
from recommender import (
    load_data, content_based_recommend,
    mood_based_recommend, get_song_details
)

app = Flask(__name__)

# Load data into memory (initialize on startup)
data = load_data()

@app.route('/')
def index():
    # Only need to pass the list of genres to the template for the sliders
    genres = ['pop', 'rap', 'rock', 'latin', 'r&b', 'edm']
    return render_template('index.html', genres=genres)

@app.route('/api/search')
def search():
    query = request.args.get('q', '').lower()
    results = []
    for s in data['songs']:
        if query in s['title'].lower() or query in s['artist'].lower():
            results.append(s)
        if len(results) >= 20: 
            break
    return jsonify(results)

@app.route('/api/songs')
def get_songs():
    # Return first 50 songs as the initial feed
    limit = int(request.args.get('limit', 50))
    return jsonify(data['songs'][:limit])

@app.route('/api/recommend/content')
def rec_content():
    try:
        song_id = int(request.args.get('song_id', 1))
    except ValueError:
        song_id = 1
    rec_ids, explanation = content_based_recommend(song_id, data)
    songs = get_song_details(rec_ids, data)
    return jsonify({"recommendations": songs, "explanation": explanation})

@app.route('/api/recommend/mood', methods=['POST'])
def rec_mood():
    weights = request.json
    # Weights should be an object: {"pop": 5, "rap": 0...}
    rec_ids, explanation = mood_based_recommend(weights, data)
    songs = get_song_details(rec_ids, data)
    return jsonify({"recommendations": songs, "explanation": explanation})

if __name__ == '__main__':
    # Maintain user's preferred port 5001
    app.run(debug=True, port=5001)
