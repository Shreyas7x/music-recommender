let currentSongs = [];

window.onload = async () => {
    try {
        const res = await fetch('/api/songs');
        const data = await res.json();
        renderSongs(data, "Explore Local Popular Tracks");
    } catch(e) {
        console.error("Failed to load initial songs", e);
    }
};

document.getElementById('search-input').addEventListener('keypress', async (e) => {
    if (e.key === 'Enter') {
        const query = e.target.value;
        if (!query) return;
        const res = await fetch(`/api/search?q=${query}`);
        const data = await res.json();
        renderSongs(data, 'Search Results');
    }
});

async function getMoodRecommendations() {
    const weights = {
        "pop": document.getElementById('mood-pop').value,
        "rap": document.getElementById('mood-rap').value,
        "rock": document.getElementById('mood-rock').value,
        "r&b": document.getElementById('mood-r&b').value,
        "latin": document.getElementById('mood-latin').value,
        "edm": document.getElementById('mood-edm').value
    };
    
    // Check if at least one slider is moved
    const totalWeights = Object.values(weights).reduce((a, b) => parseInt(a) + parseInt(b), 0);
    if (totalWeights === 0) {
        alert("Please adjust at least one mood slider!");
        return;
    }

    const btn = document.getElementById('mood-btn');
    btn.textContent = "Calculating Mood...";
    
    try {
        const res = await fetch('/api/recommend/mood', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(weights)
        });
        const data = await res.json();
        renderSongs(data.recommendations, data.explanation);
    } catch(e) {
        console.error("Error fetching mood recommendations:", e);
        renderSongs([], "Failed to fetch mood recommendations.");
    }
    btn.textContent = "Get Mood Recommendations";
}

async function recommendSimilar(songId) {
    const expBox = document.getElementById('explanation-box');
    expBox.textContent = "⌛ Finding similar songs...";
    expBox.classList.remove('hidden');

    try {
        const res = await fetch(`/api/recommend/content?song_id=${songId}`);
        const data = await res.json();
        renderSongs(data.recommendations, data.explanation);
    } catch(e) {
        console.error("Error fetching similar recommendations:", e);
    }
}

function renderSongs(songs, explanation = null) {
    currentSongs = songs;
    const container = document.getElementById('results-container');
    const expBox = document.getElementById('explanation-box');
    
    container.innerHTML = '';
    
    if (explanation) {
        expBox.textContent = `💡 ${explanation}`;
        expBox.classList.remove('hidden');
    } else {
        expBox.classList.add('hidden');
    }
    
    if (!songs || songs.length === 0) {
        container.innerHTML = `<div class="empty-state">No matching songs found. Adjust your mood sliders!</div>`;
        return;
    }
    
    songs.forEach(song => {
        const card = document.createElement('div');
        card.className = 'song-card';
        card.style.cursor = 'pointer'; // Ensure card looks clickable
        card.innerHTML = `
            <div class="song-info">
                <div class="song-title">${song.title}</div>
                <div class="song-artist">${song.artist}</div>
            </div>
            <div class="song-meta">
                <div class="song-genre">${song.genre}</div>
            </div>
        `;
        
        // Add click listener for similar song recommendations
        card.addEventListener('click', () => {
            recommendSimilar(song.id);
            window.scrollTo({ top: 0, behavior: 'smooth' }); // Scroll up to see the new list
        });
        
        container.appendChild(card);
    });
}
