import streamlit as st
import requests
import pickle
import os

API_KEY = "8265bd1679663a7ea12ac168da84d2e8"
BASE_URL = "https://api.themoviedb.org/3"
IMG_BASE = "https://image.tmdb.org/t/p/"

# ── Data loading ───────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_data():
    base_dir = os.path.dirname(__file__)
    movies_path = os.path.join(base_dir, "movie_list.pkl")
    similarity_path = os.path.join(base_dir, "similarity.pkl")
    movies = pickle.load(open(movies_path, "rb"))
    similarity = pickle.load(open(similarity_path, "rb"))
    return movies, similarity

# ── TMDB helpers ───────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False, ttl=3600)
def fetch_movie_details(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}?api_key={API_KEY}&language=en-US&append_to_response=credits,videos,similar"
    try:
        r = requests.get(url, timeout=8)
        return r.json()
    except Exception:
        return {}

@st.cache_data(show_spinner=False, ttl=3600)
def fetch_poster(movie_id, size="w500"):
    data = fetch_movie_details(movie_id)
    path = data.get("poster_path")
    if path:
        return f"{IMG_BASE}{size}{path}"
    return "https://via.placeholder.com/500x750/1a1a24/8a8890?text=No+Image"

@st.cache_data(show_spinner=False, ttl=3600)
def fetch_backdrop(movie_id):
    data = fetch_movie_details(movie_id)
    path = data.get("backdrop_path")
    if path:
        return f"{IMG_BASE}w1280{path}"
    return None

def get_trailer_url(details):
    videos = details.get("videos", {}).get("results", [])
    for v in videos:
        if v.get("type") == "Trailer" and v.get("site") == "YouTube":
            return f"https://www.youtube.com/watch?v={v['key']}"
    return None

def get_cast(details, limit=6):
    cast = details.get("credits", {}).get("cast", [])
    result = []
    for c in cast[:limit]:
        photo = c.get("profile_path")
        result.append({
            "name": c.get("name", ""),
            "character": c.get("character", ""),
            "photo": f"{IMG_BASE}w185{photo}" if photo else "https://via.placeholder.com/185x278/1a1a24/8a8890?text=?"
        })
    return result

def get_genres(details):
    return [g["name"] for g in details.get("genres", [])]

def get_rating(details):
    return round(details.get("vote_average", 0), 1)

def get_year(details):
    rd = details.get("release_date", "")
    return rd[:4] if rd else "N/A"

def get_imdb_url(details):
    imdb_id = details.get("imdb_id")
    if imdb_id:
        return f"https://www.imdb.com/title/{imdb_id}"
    return None

# ── Recommendation engine ──────────────────────────────────────────────────────
def recommend(movie_title, movies, similarity, n=5):
    idx_series = movies[movies['title'] == movie_title].index
    if len(idx_series) == 0:
        return []
    index = idx_series[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    results = []
    for i in distances[1:n+1]:
        row = movies.iloc[i[0]]
        results.append({
            "title": row["title"],
            "movie_id": int(row["movie_id"]),
            "score": round(i[1] * 100, 1)
        })
    return results

# ── Navigation ─────────────────────────────────────────────────────────────────
def nav_to(page, **kwargs):
    st.session_state.page = page
    for k, v in kwargs.items():
        st.session_state[k] = v
    st.rerun()

# ── Shared UI components ───────────────────────────────────────────────────────
def render_navbar(active="home"):
    st.markdown("### 🎬 CineMatch")
    cols = st.columns(3)
    with cols[0]:
        if st.button("Home", key="nav_home", use_container_width=True, disabled=active == "home"):
            nav_to("home")
    with cols[1]:
        if st.button("Search", key="nav_search", use_container_width=True, disabled=active == "search"):
            nav_to("search")
    with cols[2]:
        if st.button("About", key="nav_about", use_container_width=True, disabled=active == "about"):
            nav_to("about")
    st.divider()

def star_rating(score_10):
    filled = int(round(score_10 / 2))
    return "★" * filled + "☆" * (5 - filled)

def badge(text, color="#e8b84b", bg=None):
    bg = bg or "rgba(232,184,75,0.12)"
    return f'<span style="display:inline-block;padding:2px 10px;border-radius:20px;font-size:0.78rem;font-weight:600;color:{color};background:{bg};border:1px solid {color}30;margin:2px 3px 2px 0;">{text}</span>'