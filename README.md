# Music Recommender System (Pure & Minimalist)

A high-performance, dark-themed Music Recommendation System built with **Flask**, **Vanilla JS**, and **Scikit-Learn**. This version has been strictly simplified to focus on two core discovery methods: **Mood-Based Ranking** and **Click-to-Similar** discovery.

### 🌟 Features
- **Mood Sliders**: Adjust 6 genre-specific sliders (Pop, Rap, Rock, R&B, Latin, EDM) to create a custom recommendation profile.
- **Click-to-Discover**: Click on any song card to instantly find 10 similar tracks based on artist and genre similarity.
- **5,000 Track Library**: Uses a real, high-quality subset of the Spotify TidyTuesday dataset.
- **Zero-Config Local Data**: Dataset is stored locally in `spotify.csv` and `data.json` for super-fast offline use.
- **Premium Dark UI**: A modern, interactive dashboard designed for speed and clarity.

---

## core Logic & Recommendation Strategies

### 1. Mood-Based Ranking (Weighted Score)
- **How it works**: The system assigns a score to every song in the database based on your slider inputs (0-5). A song's score is derived from its matching genre weight. The list is then sorted in descending order of these scores.
- **Implementation**: See `mood_based_recommend()` in `recommender.py`.
- **UI**: Move the sliders and click **"Get Mood Recommendations"**.

### 2. Item-Item Similarity (Content-Based)
- **How it works**: Uses **TF-IDF Vectorization** on genres and artist fields. When a song is selected, the system calculates the **Cosine Similarity** between that song and every other track to find the top 10 most relevant matches.
- **Implementation**: See `content_based_recommend()` in `recommender.py`.
- **UI**: Simply **click any song card** in the results list.

---

## Getting Started

1. **Install dependencies:**
   ```bash
   pip install Flask scikit-learn numpy
   ```

2. **Launch the server:**
   ```bash
   python app.py
   ```

3. **Access the Web App:**
   Go to **`http://localhost:5001`** in your browser.

---

## File Structure
- `app.py`: Flask server and API routing.
- `recommender.py`: Core machine learning logic (TF-IDF & Mood Ranking).
- `data.json`: The processed 5,000-track dataset.
- `spotify.csv`: The raw CSV source for the 5,000-track library.
- `templates/index.html`: The minimalist dashboard.
- `static/style.css`: Modern styling for the dashboard and sliders.
- `static/script.js`: Interactive frontend logic and API calls.
