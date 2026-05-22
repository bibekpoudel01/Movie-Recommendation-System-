import streamlit as st
from utils import (fetch_movie_details, fetch_poster, fetch_backdrop,
                   nav_to, render_navbar, badge, get_year, get_rating,
                   get_genres, get_cast, get_imdb_url, get_trailer_url, star_rating)

def render():
    render_navbar("detail")

    movie_id    = st.session_state.get("detail_movie_id")
    movie_title = st.session_state.get("detail_movie_title", "Unknown")

    if not movie_id:
        st.warning("⚠️  No movie selected. Please go back and choose a movie.")
        st.divider()
        col1, col2, col3 = st.columns(3)
        with col2:
            if st.button("← Back to Search"):
                st.session_state.pop("current_recs", None)
                st.session_state.pop("current_search", None)
                nav_to("search")
        return

    st.markdown("""
    <style>
    .back-bar {
        padding: 1rem 2.5rem;
        border-bottom: 1px solid var(--border);
    }
    /* Hero backdrop */
    .backdrop-wrap {
        position: relative;
        height: 420px;
        overflow: hidden;
    }
    .backdrop-img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        filter: brightness(0.35) saturate(0.8);
        display: block;
    }
    .backdrop-overlay {
        position: absolute;
        inset: 0;
        background: linear-gradient(to right, rgba(10,10,15,0.95) 0%, rgba(10,10,15,0.5) 50%, transparent 100%),
                    linear-gradient(to top, rgba(10,10,15,1) 0%, transparent 40%);
    }
    .backdrop-content {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        display: flex;
        gap: 2rem;
        padding: 2rem 2.5rem;
        align-items: flex-end;
    }
    .detail-poster {
        width: 140px;
        min-width: 140px;
        border-radius: 10px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.7);
        border: 2px solid rgba(255,255,255,0.1);
    }
    .detail-info { flex: 1; }
    .detail-tagline {
        font-style: italic;
        color: var(--muted);
        font-size: 0.9rem;
        margin: 0 0 0.3rem;
    }
    .detail-title {
        font-family: 'Playfair Display', serif;
        font-size: clamp(1.6rem, 4vw, 2.8rem);
        font-weight: 900;
        margin: 0 0 0.6rem;
        line-height: 1.1;
        letter-spacing: -0.02em;
    }
    .detail-meta {
        display: flex;
        align-items: center;
        gap: 0.8rem;
        flex-wrap: wrap;
        margin-bottom: 0.8rem;
    }
    .detail-rating { color: var(--accent); font-weight: 700; font-size: 1rem; }
    .detail-year   { color: var(--muted); font-size: 0.9rem; }

    /* Body sections */
    .detail-body { padding: 2rem 2.5rem; }
    .section-label {
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: var(--accent);
        margin: 0 0 0.8rem;
    }
    .overview-text {
        color: #ccc;
        font-size: 0.95rem;
        line-height: 1.7;
        margin: 0 0 2rem;
        max-width: 800px;
    }

    /* Cast grid */
    .cast-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));
        gap: 0.8rem;
        margin-bottom: 2.5rem;
    }
    .cast-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 10px;
        overflow: hidden;
        text-align: center;
        transition: all 0.2s;
    }
    .cast-card:hover {
        border-color: var(--accent);
        transform: translateY(-2px);
    }
    .cast-card img { width: 100%; height: auto; max-height: 140px; object-fit: contain; display: block; }
    .cast-card-info { padding: 0.4rem 0.3rem; }
    .cast-card-name {
        font-size: 0.78rem;
        font-weight: 600;
        color: var(--text);
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
    .cast-card-char {
        font-size: 0.68rem;
        color: var(--muted);
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }

    /* Info table */
    .info-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
        gap: 1rem;
        margin-bottom: 2.5rem;
    }
    .info-item {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 1rem;
    }
    .info-key   { font-size: 0.72rem; color: var(--muted); letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 0.3rem; }
    .info-val   { font-size: 0.95rem; font-weight: 600; color: var(--text); }

    /* Link buttons */
    .ext-links { display: flex; gap: 0.8rem; flex-wrap: wrap; margin-bottom: 2.5rem; }
    .ext-btn {
        display: inline-block;
        padding: 0.55rem 1.4rem;
        border-radius: 8px;
        font-size: 0.88rem;
        font-weight: 600;
        text-decoration: none;
        border: 1px solid var(--border);
        color: var(--text);
        transition: all 0.2s;
        background: var(--surface);
    }
    .ext-btn:hover { border-color: var(--accent); color: var(--accent); background: rgba(232,184,75,0.05); }
    .ext-btn.imdb { border-color: rgba(245,197,24,0.5); color: #f5c518; }
    .ext-btn.yt   { border-color: rgba(255,0,0,0.4);   color: #ff4444; }

    /* Similar section */
    .similar-section { padding: 0 2.5rem 3rem; }
    .sim-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        overflow: hidden;
        transition: all 0.25s;
        cursor: pointer;
    }
    .sim-card:hover { border-color: var(--accent); transform: translateY(-3px); box-shadow: 0 12px 30px rgba(0,0,0,0.4); }
    .sim-card img { width: 100%; aspect-ratio: 2/3; object-fit: cover; }
    .sim-card-body { padding: 0.7rem; }
    .sim-card-title { font-size: 0.85rem; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .sim-card-meta  { font-size: 0.75rem; color: var(--muted); }
    </style>
    """, unsafe_allow_html=True)

    # Back button
    st.markdown('<div class="back-bar">', unsafe_allow_html=True)
    if st.button("← Back to Search"):
        st.session_state.pop("detail_movie_id", None)
        st.session_state.pop("detail_movie_title", None)
        nav_to("search")
    st.markdown('</div>', unsafe_allow_html=True)

    # Load details
    with st.spinner("Loading movie details…"):
        details   = fetch_movie_details(movie_id)
        poster    = fetch_poster(movie_id, size="w342")
        backdrop  = fetch_backdrop(movie_id)
        cast      = get_cast(details, limit=6)
        imdb_url  = get_imdb_url(details)
        trailer   = get_trailer_url(details)

    title    = details.get("title", movie_title)
    tagline  = details.get("tagline", "")
    overview = details.get("overview", "No overview available.")
    year     = get_year(details)
    rating   = get_rating(details)
    genres   = get_genres(details)
    runtime  = details.get("runtime", 0)
    budget   = details.get("budget", 0)
    revenue  = details.get("revenue", 0)
    lang     = details.get("original_language", "").upper()
    votes    = details.get("vote_count", 0)
    stars    = star_rating(rating)
    genre_badges = "".join(badge(g) for g in genres)

    # ── Backdrop Hero ─────────────────────────────────────────────────────────
    backdrop_tag = f'<img class="backdrop-img" src="{backdrop}" alt="">' if backdrop else \
                   '<div class="backdrop-img" style="background:var(--surface2);"></div>'

    st.markdown(f"""
    <div class="backdrop-wrap">
        {backdrop_tag}
        <div class="backdrop-overlay"></div>
        <div class="backdrop-content">
            <img class="detail-poster" src="{poster}" alt="{title}">
            <div class="detail-info">
                {f'<p class="detail-tagline">"{tagline}"</p>' if tagline else ""}
                <h1 class="detail-title">{title}</h1>
                <div class="detail-meta">
                    <span class="detail-rating">{stars} {rating}/10</span>
                    <span style="color:var(--border)">·</span>
                    <span class="detail-year">{year}</span>
                    {f'<span style="color:var(--border)">·</span><span style="color:var(--muted);font-size:0.85rem;">{runtime} min</span>' if runtime else ""}
                    <span style="color:var(--border)">·</span>
                    {genre_badges}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Body ──────────────────────────────────────────────────────────────────
    st.markdown('<div class="detail-body">', unsafe_allow_html=True)

    # External links
    links_html = ""
    if imdb_url:
        links_html += f'<a class="ext-btn imdb" href="{imdb_url}" target="_blank">⭐ View on IMDb</a>'
    if trailer:
        links_html += f'<a class="ext-btn yt" href="{trailer}" target="_blank">▶ Watch Trailer</a>'
    if links_html:
        st.markdown(f'<div class="ext-links">{links_html}</div>', unsafe_allow_html=True)

    # Overview
    st.markdown(f'<p class="section-label">Overview</p><p class="overview-text">{overview}</p>', unsafe_allow_html=True)

    # Cast
    if cast:
        st.markdown('<p class="section-label">Cast</p><div class="cast-grid">', unsafe_allow_html=True)
        for c in cast:
            st.markdown(f"""
            <div class="cast-card">
                <img src="{c["photo"]}" alt="{c["name"]}">
                <div class="cast-card-info">
                    <div class="cast-card-name" title="{c["name"]}">{c["name"]}</div>
                    <div class="cast-card-char" title="{c["character"]}">{c["character"]}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Info grid
    info_items = [
        ("Release Year", year),
        ("Rating", f"★ {rating} / 10  ({votes:,} votes)" if votes else f"★ {rating}"),
        ("Runtime", f"{runtime} min" if runtime else "—"),
        ("Language", lang or "—"),
        ("Budget",  f"${budget/1e6:.1f}M"  if budget  else "—"),
        ("Revenue", f"${revenue/1e6:.1f}M" if revenue else "—"),
    ]
    items_html = "".join(f'<div class="info-item"><div class="info-key">{k}</div><div class="info-val">{v}</div></div>' for k, v in info_items)
    st.markdown(f'<p class="section-label">Details</p><div class="info-grid">{items_html}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ── Similar from TMDB ─────────────────────────────────────────────────────
    similar = details.get("similar", {}).get("results", [])[:6]
    if similar:
        st.markdown("""
        <div style="padding:0 2.5rem 1rem;border-top:1px solid var(--border);">
            <p class="section-label" style="margin-top:2rem;">You Might Also Like</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="similar-section"><div style="display:grid;grid-template-columns:repeat(6,1fr);gap:1rem;">', unsafe_allow_html=True)
        cols = st.columns(len(similar), gap="small")
        for col, sm in zip(cols, similar):
            sm_id    = sm.get("id")
            sm_title = sm.get("title", "")
            sm_year  = (sm.get("release_date") or "")[:4]
            sm_rat   = round(sm.get("vote_average", 0), 1)
            sm_post  = fetch_poster(sm_id) if sm_id else ""
            with col:
                st.markdown(f"""
                <div class="sim-card">
                    <img src="{sm_post}" alt="{sm_title}">
                    <div class="sim-card-body">
                        <div class="sim-card-title" title="{sm_title}">{sm_title}</div>
                        <div class="sim-card-meta">★ {sm_rat} · {sm_year}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("→", key=f"sim_{sm_id}", use_container_width=True):
                    nav_to("detail", detail_movie_id=sm_id, detail_movie_title=sm_title)
        st.markdown('</div></div>', unsafe_allow_html=True)