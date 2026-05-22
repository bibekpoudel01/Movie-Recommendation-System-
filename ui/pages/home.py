import streamlit as st
from utils import (load_data, fetch_movie_details, fetch_poster,
                   nav_to, render_navbar, get_year, get_rating, get_genres)

FEATURED_IDS = [550, 27205, 238, 157336, 680, 278]


def render():
    render_navbar("home")

    st.markdown("""
    <style>
    .hero {
        position: relative;
        padding: 5rem 3rem 3.5rem;
        text-align: center;
        background: radial-gradient(ellipse 80% 55% at 50% -5%,  rgba(232,184,75,0.16) 0%, transparent 65%),
                    radial-gradient(ellipse 55% 35% at 85% 90%,  rgba(192,57,43,0.09) 0%, transparent 60%);
        overflow: hidden;
    }
    .hero-eyebrow {
        font-size: 0.73rem; font-weight: 600;
        letter-spacing: 0.22em; color: var(--accent);
        text-transform: uppercase; margin-bottom: 1rem;
    }
    .hero-title {
        font-family: 'Playfair Display', serif;
        font-size: clamp(2.6rem, 5.5vw, 4.8rem);
        font-weight: 900; line-height: 1.06;
        letter-spacing: -0.03em; margin: 0 0 1.1rem;
        background: linear-gradient(135deg, #f0eee8 0%, var(--accent) 55%, #f0eee8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .hero-sub {
        font-size: 1.05rem; color: var(--muted);
        max-width: 500px; margin: 0 auto 2.5rem;
        line-height: 1.65; font-weight: 300;
    }
    .hero-stats {
        display: flex; justify-content: center; gap: 3rem;
        margin-top: 2.8rem; padding-top: 2.2rem;
        border-top: 1px solid var(--border);
    }
    .stat-num {
        display: block;
        font-family: 'Playfair Display', serif;
        font-size: 2rem; font-weight: 700; color: var(--accent);
    }
    .stat-label {
        font-size: 0.73rem; color: var(--muted);
        text-transform: uppercase; letter-spacing: 0.12em; font-weight: 500;
    }

    /* Featured cards */
    .feat-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        overflow: hidden;
        transition: border-color 0.25s, transform 0.25s, box-shadow 0.25s;
    }
    .feat-card:hover {
        border-color: var(--accent);
        transform: translateY(-5px);
        box-shadow: 0 18px 40px rgba(0,0,0,0.45), 0 0 0 1px rgba(232,184,75,0.18);
    }
    .feat-card img { width:100%; aspect-ratio:2/3; object-fit:cover; display:block; }
    .feat-body  { padding: 0.85rem; }
    .feat-title {
        font-family: 'Playfair Display', serif;
        font-size: 0.88rem; font-weight: 700;
        margin: 0 0 0.25rem; white-space: nowrap;
        overflow: hidden; text-overflow: ellipsis; color: var(--text);
    }
    .feat-meta { font-size: 0.74rem; color: var(--muted); }
    .feat-rating { color: var(--accent); font-weight: 600; }

    .section-hdr {
        padding: 2.2rem 2.5rem 0.9rem;
        display: flex; align-items: baseline; gap: 0.9rem;
    }
    .section-hdr h2 {
        font-family: 'Playfair Display', serif;
        font-size: 1.5rem; font-weight: 700; margin: 0; color: var(--text);
    }
    .section-hdr span { font-size: 0.82rem; color: var(--muted); }
    </style>
    """, unsafe_allow_html=True)

    # ── Hero ──────────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="hero">
        <p class="hero-eyebrow">✦ AI-Powered Discovery</p>
        <h1 class="hero-title">Find Your Next<br>Favourite Film</h1>
        <p class="hero-sub">Intelligent recommendations tailored to your taste.
           Explore detailed cast info and dive deep into cinema.</p>
    </div>
    """, unsafe_allow_html=True)

    # CTA button — centred with columns (fixed: no tuple unpacking bug)
    cols = st.columns([3, 2, 3])
    with cols[1]:
        if st.button("🔍  Search & Get Recommendations", use_container_width=True):
            nav_to("search")

    # Stats
    try:
        movies, _ = load_data()
        n_movies  = f"{len(movies):,}"
    except Exception:
        n_movies  = "5,000+"

    st.markdown(f"""
    <div class="hero-stats">
        <div><span class="stat-num">{n_movies}</span><span class="stat-label">Movies</span></div>
        <div><span class="stat-num">∞</span>         <span class="stat-label">Discoveries</span></div>
        <div><span class="stat-num">5★</span>        <span class="stat-label">Quality Picks</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr style="margin:0;">', unsafe_allow_html=True)

    # ── Featured Grid ─────────────────────────────────────────────────────────
    st.markdown("""
    <div class="section-hdr">
        <h2>Featured Films</h2>
        <span>Handpicked classics &amp; modern masterpieces</span>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(6, gap="small")
    for idx, (col, mid) in enumerate(zip(cols, FEATURED_IDS)):
        with col:
            details   = fetch_movie_details(mid)
            poster    = fetch_poster(mid)
            title     = details.get("title", "Unknown")
            year      = get_year(details)
            rating    = get_rating(details)
            genres    = get_genres(details)
            genre_txt = genres[0] if genres else ""

            st.markdown(f"""
            <div class="feat-card">
                <img src="{poster}" alt="{title}">
                <div class="feat-body">
                    <p class="feat-title" title="{title}">{title}</p>
                    <div class="feat-meta">
                        <span class="feat-rating">★ {rating}</span>
                        &nbsp;·&nbsp;{year}
                        {"&nbsp;·&nbsp;" + genre_txt if genre_txt else ""}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # ← this button WORKS because nav_to sets state then reruns
            if st.button("Details", key=f"home_feat_{idx}", use_container_width=True):
                nav_to("detail", detail_movie_id=mid, detail_movie_title=title)

    # ── CTA banner ────────────────────────────────────────────────────────────
    st.markdown("""
    <div style="text-align:center;padding:3rem 2rem;margin-top:1.5rem;
                background:linear-gradient(135deg,rgba(232,184,75,0.05) 0%,rgba(192,57,43,0.05) 100%);
                border-top:1px solid var(--border);border-bottom:1px solid var(--border);">
        <p style="font-family:'Playfair Display',serif;font-size:1.7rem;font-weight:700;margin:0 0 0.4rem;">
            Ready to discover?</p>
        <p style="color:var(--muted);margin:0 0 1.4rem;font-size:0.93rem;">
            Search any movie and get 5 personalised recommendations instantly.</p>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns([3, 2, 3])
    with cols[1]:
        if st.button("🎬  Get Recommendations", key="home_cta", use_container_width=True):
            nav_to("search")