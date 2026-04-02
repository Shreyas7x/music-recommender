import json
import random
import os
import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

DATA_PATH = os.path.join(os.path.dirname(__file__), 'data.json')
CSV_PATH = os.path.join(os.path.dirname(__file__), 'spotify.csv')

def load_data():
    if not os.path.exists(DATA_PATH):
        # This shouldn't be needed anymore as we generated data previously,
        # but kept as a small safety for the project structure.
        return {"songs": [], "users": []}
    with open(DATA_PATH, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_PATH, 'w') as f:
        json.dump(data, f, indent=4)

def get_song_details(song_ids, data):
    songs_map = {s['id']: s for s in data['songs']}
    return [songs_map[sid] for sid in song_ids if sid in songs_map]

def content_based_recommend(song_id, data, top_n=10):
    songs = data['songs']
    song_map = {s['id']: idx for idx, s in enumerate(songs)}
    reverse_song_map = {idx: s['id'] for idx, s in enumerate(songs)}
    
    if song_id not in song_map:
        return [], "Song not found"
        
    # Use genre and artist for metadata similarity
    documents = [f"{s['genre']} {s['artist']}" for s in songs]
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(documents)
    
    target_idx = song_map[song_id]
    similarities = cosine_similarity(tfidf_matrix[target_idx:target_idx+1], tfidf_matrix).flatten()
    
    # Exclude the target song itself
    similarities[target_idx] = -1
    
    top_indices = similarities.argsort()[::-1][:top_n]
    return [reverse_song_map[idx] for idx in top_indices], "Recommended based on song similarity"

def mood_based_recommend(genre_weights, data, top_n=15):
    """
    Ranks songs based on a weighted profile of genres.
    genre_weights: e.g., {"pop": 5, "rap": 4, "rock": 0, ...}
    """
    songs = data['songs']
    
    # Normalize weights
    weights = {k.lower(): float(v) for k, v in genre_weights.items()}
    
    scored_songs = []
    for s in songs:
        genre = s['genre'].lower()
        base_score = weights.get(genre, 0)
        
        if base_score > 0:
            # We add a tiny bit of random noise (0.01) to keep the list fresh
            # and sort by the selected weights.
            final_score = base_score + (random.random() * 0.01)
            scored_songs.append((s['id'], final_score))
            
    # Sort by score descending (highest weights first)
    scored_songs.sort(key=lambda x: x[1], reverse=True)
    
    top_ids = [item[0] for item in scored_songs[:top_n]]
    
    if not top_ids:
        return [], "No matching songs found for these genre weights."
        
    explanation = "Sorted by matching mood: " + ", ".join([f"{g.capitalize()} ({int(w)})" for g, w in weights.items() if w > 1])
    return top_ids, explanation
