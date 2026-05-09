import streamlit as st
from utils import render_navbar


def render():
    render_navbar("about")

    st.markdown("""
    <style>
    .about-hero {
        padding: 4rem 3rem 2.5rem;
        background: radial-gradient(ellipse 70% 60% at 20% 0%, rgba(232,184,75,0.12) 0%, transparent 60%),
                    radial-gradient(ellipse 60% 40% at 85% 80%, rgba(192,57,43,0.08) 0%, transparent 65%);
        border-bottom: 1px solid var(--border);
        text-align: left;
    }
    .about-eyebrow {
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.2em;
        color: var(--accent);
        text-transform: uppercase;
        margin-bottom: 1rem;
    }
    .about-title {
        font-family: 'Playfair Display', serif;
        font-size: clamp(2.4rem, 5vw, 4rem);
        font-weight: 900;
        line-height: 1.08;
        margin: 0 0 1rem;
        letter-spacing: -0.03em;
    }
    .about-sub {
        color: var(--muted);
        max-width: 720px;
        font-size: 1rem;
        line-height: 1.7;
        margin: 0;
    }

    .about-section {
        padding: 2.5rem 2.5rem 0;
    }
    .section-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.5rem;
        font-weight: 700;
        margin: 0 0 1rem;
    }
    .section-sub {
        color: var(--muted);
        font-size: 0.9rem;
        margin: 0 0 1.4rem;
    }

    .card-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 1.2rem;
    }
    .info-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 1.2rem;
        transition: all 0.2s ease;
    }
    .info-card:hover {
        border-color: var(--accent);
        transform: translateY(-2px);
        box-shadow: 0 10px 24px rgba(0,0,0,0.35);
    }
    .card-title {
        font-weight: 700;
        margin: 0 0 0.4rem;
        color: var(--text);
        font-size: 0.98rem;
    }
    .card-body {
        color: var(--muted);
        font-size: 0.85rem;
        line-height: 1.6;
        margin: 0;
    }

    .timeline {
        display: grid;
        grid-template-columns: 1fr;
        gap: 0.9rem;
    }
    .timeline-item {
        display: grid;
        grid-template-columns: 28px 1fr;
        gap: 0.8rem;
        align-items: start;
    }
    .dot {
        width: 10px;
        height: 10px;
        margin-top: 6px;
        border-radius: 50%;
        background: var(--accent);
        box-shadow: 0 0 0 4px rgba(232,184,75,0.15);
    }
    .timeline-title {
        font-weight: 700;
        margin: 0 0 0.2rem;
        font-size: 0.95rem;
    }
    .timeline-text {
        color: var(--muted);
        margin: 0;
        font-size: 0.85rem;
        line-height: 1.6;
    }

    .pill-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.6rem;
    }
    .pill {
        padding: 6px 12px;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 600;
        color: var(--text);
        border: 1px solid var(--border);
        background: var(--surface2);
    }
    </style>

    <div class="about-hero">
        <p class="about-eyebrow">About</p>
        <h1 class="about-title">CineMatch is your personal movie guide</h1>
        <p class="about-sub">
            CineMatch blends a content-based recommender with live movie metadata to help you discover
            films that match your taste. The experience is designed to be fast, visual, and focused on
            meaningful details so you can decide what to watch in seconds.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="about-section">
        <h2 class="section-title">What makes it special</h2>
        <p class="section-sub">A simple flow that keeps the focus on discovery.</p>
        <div class="card-grid">
            <div class="info-card">
                <p class="card-title">Smart similarity engine</p>
                <p class="card-body">Finds movies with matching story themes, genres, and style based on vector similarity.</p>
            </div>
            <div class="info-card">
                <p class="card-title">Live movie details</p>
                <p class="card-body">Pulls fresh posters, ratings, cast, and trailers from TMDB to enrich every result.</p>
            </div>
            <div class="info-card">
                <p class="card-title">Focused UI</p>
                <p class="card-body">A dark, cinematic layout that highlights what matters and keeps distractions away.</p>
            </div>
            <div class="info-card">
                <p class="card-title">Fast navigation</p>
                <p class="card-body">Jump between search, details, and recommendations without losing context.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="about-section">
        <h2 class="section-title">How it works</h2>
        <p class="section-sub">From input to recommendations in three steps.</p>
        <div class="timeline">
            <div class="timeline-item">
                <div class="dot"></div>
                <div>
                    <p class="timeline-title">1. Choose a movie you like</p>
                    <p class="timeline-text">Select a title from the dataset to anchor your taste profile.</p>
                </div>
            </div>
            <div class="timeline-item">
                <div class="dot"></div>
                <div>
                    <p class="timeline-title">2. Similarity scoring</p>
                    <p class="timeline-text">The engine ranks movies by content similarity and returns the closest matches.</p>
                </div>
            </div>
            <div class="timeline-item">
                <div class="dot"></div>
                <div>
                    <p class="timeline-title">3. Explore the details</p>
                    <p class="timeline-text">Dive into cast, trailers, and extra context before making a pick.</p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="about-section">
        <h2 class="section-title">Built with</h2>
        <p class="section-sub">A focused stack that keeps the app fast and maintainable.</p>
        <div class="pill-row">
            <span class="pill">Streamlit</span>
            <span class="pill">Pandas</span>
            <span class="pill">scikit-learn</span>
            <span class="pill">TMDB API</span>
            <span class="pill">Python</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="about-section" style="padding-bottom:3rem;">
        <h2 class="section-title">Data sources and notes</h2>
        <p class="section-sub">Credits and important info.</p>
        <div class="card-grid">
            <div class="info-card">
                <p class="card-title">TMDB</p>
                <p class="card-body">Movie metadata and imagery come from The Movie Database (TMDB) API.</p>
            </div>
            <div class="info-card">
                <p class="card-title">Local dataset</p>
                <p class="card-body">Recommendations are computed from the local movie list and similarity matrix.</p>
            </div>
            <div class="info-card">
                <p class="card-title">Privacy</p>
                <p class="card-body">No personal data is stored. Your choices stay in the session only.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
