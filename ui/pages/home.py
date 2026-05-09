import streamlit as st
from utils import load_data, fetch_movie_details, fetch_poster, recommend, nav_to, render_navbar, badge, get_year, get_rating, get_genres

FEATURED_IDS = [550, 27205, 238, 157336, 680, 278]  # Fight Club, Inception, Godfather, Interstellar, Pulp Fiction, Shawshank


def render():
    render_navbar("home")

    # ── Hero Section ──────────────────────────────────────────────────────────
    st.markdown("""
    <style>
    .hero {
        position: relative;
        padding: 6rem 3rem 4rem;
        text-align: center;
        overflow: hidden;
        background: radial-gradient(ellipse 80% 60% at 50% -10%, rgba(232,184,75,0.18) 0%, transparent 60%),
                    radial-gradient(ellipse 60% 40% at 80% 80%, rgba(192,57,43,0.1) 0%, transparent 60%);
    }
    .hero::before {
        content: '';
        position: absolute;
        inset: 0;
        background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.02'%3E%3Ccircle cx='1' cy='1' r='1'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        pointer-events: none;
    }
    .hero-eyebrow {
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.2em;
        color: var(--accent);
        text-transform: uppercase;
        margin-bottom: 1rem;
    }
    .hero-title {
        font-family: 'Playfair Display', serif;
        font-size: clamp(2.8rem, 6vw, 5rem);
        font-weight: 900;
        line-height: 1.05;
        letter-spacing: -0.03em;
        margin: 0 0 1.2rem;
        background: linear-gradient(135deg, #f0eee8 0%, var(--accent) 50%, #f0eee8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .hero-sub {
        font-size: 1.1rem;
        color: var(--muted);
        max-width: 520px;
        margin: 0 auto 2.5rem;
        line-height: 1.6;
        font-weight: 300;
    }
    .hero-stats {
        display: flex;
        justify-content: center;
        gap: 3rem;
        margin-top: 3rem;
        padding-top: 2.5rem;
        border-top: 1px solid var(--border);
    }
    .stat { text-align: center; }
    .stat-num {
        font-family: 'Playfair Display', serif;
        font-size: 2.2rem;
        font-weight: 700;
        color: var(--accent);
        display: block;
    }
    .stat-label {
        font-size: 0.78rem;
        color: var(--muted);
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-weight: 500;
    }

    /* Movie card */
    .movie-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        overflow: hidden;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        height: 100%;
    }
    .movie-card:hover {
        border-color: var(--accent);
        transform: translateY(-4px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.4), 0 0 0 1px rgba(232,184,75,0.2);
    }
    .movie-card img {
        width: 100%;
        aspect-ratio: 2/3;
        object-fit: cover;
        display: block;
    }
    .card-body { padding: 1rem; }
    .card-title {
        font-family: 'Playfair Display', serif;
        font-size: 0.95rem;
        font-weight: 700;
        margin: 0 0 0.3rem;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        color: var(--text);
    }
    .card-meta {
        font-size: 0.78rem;
        color: var(--muted);
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .card-rating { color: var(--accent); font-weight: 600; }

    /* Section headers */
    .section-header {
        padding: 2.5rem 2.5rem 1rem;
        display: flex;
        align-items: baseline;
        gap: 1rem;
    }
    .section-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.6rem;
        font-weight: 700;
        margin: 0;
        color: var(--text);
    }
    .section-sub { font-size: 0.85rem; color: var(--muted); }

    .cards-grid { padding: 0 2rem 3rem; }
    </style>

    <div class="hero">
        <p class="hero-eyebrow">✦ AI-Powered Discovery</p>
        <h1 class="hero-title">Find Your Next<br>Favourite Film</h1>
        <p class="hero-sub">Intelligent recommendations tailored to your taste. Discover hidden gems, explore detailed cast info, and dive deep into cinema.</p>
    </div>
    """, unsafe_allow_html=True)

    # CTA Buttons
    _, c1, c2, _ = st.columns([3, 1.2, 1.2, 3], gap="small") # center the buttons
    with c1:
        if st.button("🔍  Search Movies", use_container_width=True):
            nav_to("search")
    with c2:
        st.markdown('<div style="height:100%;display:flex;align-items:center;justify-content:center;color:var(--muted);font-size:0.85rem;">or explore below ↓</div>', unsafe_allow_html=True)

    # Stats row
    try:
        movies, _ = load_data()
        n_movies = len(movies)
    except Exception:
        n_movies = "5,000+"

    st.markdown(f"""
    <div class="hero-stats">
        <div class="stat"><span class="stat-num">{n_movies}</span><span class="stat-label">Movies</span></div>
        <div class="stat"><span class="stat-num">∞</span><span class="stat-label">Discoveries</span></div>
        <div class="stat"><span class="stat-num">5★</span><span class="stat-label">Quality Picks</span></div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<hr style="margin:0;border-color:var(--border);">', unsafe_allow_html=True)

    # ── Featured Movies Grid ──────────────────────────────────────────────────
    st.markdown('<div class="section-header"><h2 class="section-title">Featured Films</h2><span class="section-sub">Handpicked classics & modern masterpieces</span></div>', unsafe_allow_html=True)

    st.markdown('<div class="cards-grid">', unsafe_allow_html=True)
    cols = st.columns(6, gap="medium")
    for idx, (col, mid) in enumerate(zip(cols, FEATURED_IDS)):
        with col:
            with st.spinner(""):
                details = fetch_movie_details(mid)
            poster = fetch_poster(mid)
            title = details.get("title", "Unknown")
            year = get_year(details)
            rating = get_rating(details)
            genres = get_genres(details)[:1]
            genre_txt = genres[0] if genres else ""

            st.markdown(f"""
            <div class="movie-card">
                <img src="{poster}" alt="{title}">
                <div class="card-body">
                    <p class="card-title" title="{title}">{title}</p>
                    <div class="card-meta">
                        <span class="card-rating">★ {rating}</span>
                        <span>·</span>
                        <span>{year}</span>
                        {'<span>· </span><span>' + genre_txt + '</span>' if genre_txt else ''}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("Details", key=f"feat_{idx}", use_container_width=True):
                nav_to("detail", detail_movie_id=mid, detail_movie_title=title)

    st.markdown('</div>', unsafe_allow_html=True)

    # ── Quick search CTA ──────────────────────────────────────────────────────
    st.markdown("""
    <div style="text-align:center;padding:3rem 2rem;background:linear-gradient(135deg,rgba(232,184,75,0.05) 0%,rgba(192,57,43,0.05) 100%);border-top:1px solid var(--border);border-bottom:1px solid var(--border);">
        <p style="font-family:'Playfair Display',serif;font-size:1.8rem;font-weight:700;margin:0 0 0.5rem;">Ready to discover?</p>
        <p style="color:var(--muted);margin:0 0 1.5rem;font-size:0.95rem;">Search any movie and get 5 personalised recommendations instantly.</p>
    </div>
    """, unsafe_allow_html=True)

    _, mid_col, _ = st.columns([2, 2, 2])
    with mid_col:
        if st.button("🎬  Get Recommendations", use_container_width=True):
            nav_to("search")