import streamlit as st
from utils import (load_data, fetch_movie_details, fetch_poster, recommend,
                   nav_to, render_navbar, badge, get_year, get_rating, get_genres,
                   get_trailer_url, get_cast, get_imdb_url, star_rating)

def render():
    render_navbar("search")

    st.markdown("""
    <style>
    .search-hero {
        padding: 3rem 3rem 2rem;
        background: linear-gradient(180deg, rgba(232,184,75,0.06) 0%, transparent 100%);
        border-bottom: 1px solid var(--border);
    }
    .search-title {
        font-family: 'Playfair Display', serif;
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0 0 0.4rem;
        letter-spacing: -0.02em;
    }
    .search-sub { color: var(--muted); font-size: 0.95rem; margin: 0 0 2rem; }

    /* Rec card ── big horizontal card */
    .rec-card {
        display: flex;
        gap: 1.5rem;
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        overflow: hidden;
        margin-bottom: 1.2rem;
        transition: all 0.25s cubic-bezier(0.4,0,0.2,1);
    }
    .rec-card:hover {
        border-color: var(--accent);
        box-shadow: 0 8px 32px rgba(0,0,0,0.35), 0 0 0 1px rgba(232,184,75,0.15);
        transform: translateX(4px);
    }
    .rec-poster {
        width: 110px;
        min-width: 110px;
        aspect-ratio: 2/3;
        object-fit: cover;
    }
    .rec-body {
        padding: 1.2rem 1.2rem 1.2rem 0;
        flex: 1;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-width: 0;
    }
    .rec-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.1rem;
        font-weight: 700;
        margin: 0 0 0.3rem;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .rec-overview {
        font-size: 0.83rem;
        color: var(--muted);
        line-height: 1.55;
        margin: 0.4rem 0 0.8rem;
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }
    .rec-meta {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        flex-wrap: wrap;
        margin-bottom: 0.8rem;
    }
    .rec-rating { color: var(--accent); font-weight: 700; font-size: 0.88rem; }
    .rec-year   { color: var(--muted);  font-size: 0.82rem; }
    .rec-match  {
        background: rgba(232,184,75,0.12);
        color: var(--accent);
        font-size: 0.75rem;
        font-weight: 600;
        padding: 2px 8px;
        border-radius: 20px;
        border: 1px solid rgba(232,184,75,0.3);
    }
    .rec-actions { display: flex; gap: 0.5rem; flex-wrap: wrap; }
    .link-pill {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 600;
        text-decoration: none;
        border: 1px solid var(--border);
        color: var(--muted);
        transition: all 0.2s;
    }
    .link-pill:hover { border-color: var(--accent); color: var(--accent); }
    .link-pill.imdb { border-color: rgba(245,197,24,0.4); color: #f5c518; }
    .link-pill.trailer { border-color: rgba(255,0,0,0.3); color: #ff4444; }

    /* Cast strip */
    .cast-strip {
        display: flex;
        gap: 0.6rem;
        overflow-x: auto;
        padding-bottom: 4px;
        scrollbar-width: thin;
    }
    .cast-item { text-align: center; min-width: 60px; }
    .cast-item img {
        width: 52px;
        height: 52px;
        border-radius: 50%;
        object-fit: cover;
        border: 2px solid var(--border);
    }
    .cast-name {
        font-size: 0.65rem;
        color: var(--muted);
        margin-top: 4px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 60px;
    }

    /* Results header */
    .results-header {
        display: flex;
        align-items: center;
        gap: 0.8rem;
        padding: 2rem 2.5rem 1rem;
    }
    .results-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.4rem;
        font-weight: 700;
        margin: 0;
    }
    .results-count {
        background: var(--surface2);
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 2px 10px;
        font-size: 0.78rem;
        color: var(--muted);
    }
    .results-body { padding: 0 2.5rem 3rem; }
    </style>

    <div class="search-hero">
        <h1 class="search-title">Search & Discover</h1>
        <p class="search-sub">Type a movie title to get 5 personalised recommendations</p>
    """, unsafe_allow_html=True)

    # ── Load data ─────────────────────────────────────────────────────────────
    try:
        movies, similarity = load_data()
        movie_list = sorted(movies['title'].values.tolist())
        data_ok = True
    except Exception as e:
        st.error(f"⚠️  Could not load movie data: {e}\n\nMake sure `movie_list.pkl` and `similarity.pkl` are in the app directory.")
        data_ok = False
        movie_list = []

    # ── Search controls ────────────────────────────────────────────────────────
    col_sel, col_btn = st.columns([5, 1], gap="small")
    with col_sel:
        selected = st.selectbox(
            "Select a movie",
            options=movie_list if data_ok else ["(no data)"],
            index=0,
            label_visibility="collapsed"
        )
    with col_btn:
        search_clicked = st.button("✨  Recommend", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)  # close search-hero

    # ── Recommendations ────────────────────────────────────────────────────────
    if search_clicked and data_ok and selected:
        recs = recommend(selected, movies, similarity, n=5)

        st.markdown(f"""
        <div class="results-header">
            <h2 class="results-title">Because you like <em>{selected}</em></h2>
            <span class="results-count">{len(recs)} picks</span>
        </div>
        <div class="results-body">
        """, unsafe_allow_html=True)

        for i, rec in enumerate(recs):
            mid = rec["movie_id"]
            with st.spinner(f"Loading {rec['title']}…"):
                details = fetch_movie_details(mid)
            poster = fetch_poster(mid)
            title = details.get("title") or rec["title"]
            year = get_year(details)
            rating = get_rating(details)
            genres = get_genres(details)
            overview = details.get("overview", "No overview available.")
            cast = get_cast(details, limit=5)
            imdb_url = get_imdb_url(details)
            trailer_url = get_trailer_url(details)
            score = rec["score"]

            genre_badges = "".join(badge(g) for g in genres[:3])
            stars = star_rating(rating)

            # Cast avatars HTML
            cast_html = '<div class="cast-strip">'
            for c in cast:
                cast_html += f'''<div class="cast-item">
                    <img src="{c["photo"]}" alt="{c["name"]}">
                    <div class="cast-name" title="{c["name"]} as {c["character"]}">{c["name"].split()[0]}</div>
                </div>'''
            cast_html += '</div>'

            # Links
            links_html = ""
            if imdb_url:
                links_html += f'<a class="link-pill imdb" href="{imdb_url}" target="_blank">⭐ IMDb</a>'
            if trailer_url:
                links_html += f'<a class="link-pill trailer" href="{trailer_url}" target="_blank">▶ Trailer</a>'

            st.markdown(f"""
            <div class="rec-card">
                <img class="rec-poster" src="{poster}" alt="{title}">
                <div class="rec-body">
                    <div>
                        <div style="display:flex;align-items:center;gap:0.6rem;margin-bottom:0.2rem;">
                            <p class="rec-title">{i+1}. {title}</p>
                            <span class="rec-match">↑ {score}% match</span>
                        </div>
                        <div class="rec-meta">
                            <span class="rec-rating">{stars} {rating}/10</span>
                            <span style="color:var(--border)">·</span>
                            <span class="rec-year">{year}</span>
                            <span style="color:var(--border)">·</span>
                            {genre_badges}
                        </div>
                        <p class="rec-overview">{overview}</p>
                        {cast_html}
                    </div>
                    <div class="rec-actions" style="margin-top:0.8rem;">
                        {links_html}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Streamlit button for detail page (visually below the card)
            if st.button(f"🎬 Full Details — {title}", key=f"detail_{i}"):
                nav_to("detail", detail_movie_id=mid, detail_movie_title=title)

        st.markdown('</div>', unsafe_allow_html=True)

    elif not data_ok:
        st.markdown("""
        <div style="padding:4rem 2.5rem;text-align:center;color:var(--muted);">
            <p style="font-size:3rem;margin:0;">📦</p>
            <p style="font-family:'Playfair Display',serif;font-size:1.3rem;color:var(--text);margin:1rem 0 0.5rem;">Data files not found</p>
            <p>Place <code>movie_list.pkl</code> and <code>similarity.pkl</code> in the app root directory.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="padding:5rem 2.5rem;text-align:center;color:var(--muted);">
            <p style="font-size:3rem;margin:0 0 0.5rem;">🎬</p>
            <p style="font-size:1rem;">Select a movie above and click <strong style="color:var(--accent);">✨ Recommend</strong> to discover similar films</p>
        </div>
        """, unsafe_allow_html=True)