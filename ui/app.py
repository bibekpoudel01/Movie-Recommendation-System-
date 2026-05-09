import streamlit as st

st.set_page_config(
    page_title="CineMatch — Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Inject global CSS ──────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --bg:        #0a0a0f;
    --surface:   #111118;
    --surface2:  #1a1a24;
    --border:    rgba(255,255,255,0.07);
    --accent:    #e8b84b;
    --accent2:   #c0392b;
    --text:      #f0eee8;
    --muted:     #8a8890;
    --radius:    14px;
}

/* Reset */
html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stHeader"], [data-testid="stToolbar"] { display:none !important; }
[data-testid="stSidebar"] { display:none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stMain"] > div { padding: 0 !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: #333; border-radius: 3px; }

/* Buttons */
.stButton > button {
    background: var(--accent) !important;
    color: #000 !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.03em !important;
    padding: 0.55rem 1.4rem !important;
    transition: all 0.2s !important;
    cursor: pointer !important;
}
.stButton > button:hover {
    background: #f5c842 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(232,184,75,0.3) !important;
}

/* Selectbox */
[data-testid="stSelectbox"] > div > div {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
}

/* Text input */
[data-testid="stTextInput"] input {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* Expander */
[data-testid="stExpander"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
}

/* Divider */
hr { border-color: var(--border) !important; }

/* Spinner */
[data-testid="stSpinner"] { color: var(--accent) !important; }

/* Hide streamlit branding */
footer { display:none !important; }
</style>
""", unsafe_allow_html=True)

# ── Page router ────────────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "home"
if "selected_movie" not in st.session_state:
    st.session_state.selected_movie = None
if "detail_movie_id" not in st.session_state:
    st.session_state.detail_movie_id = None
if "detail_movie_title" not in st.session_state:
    st.session_state.detail_movie_title = None

page = st.session_state.page

if page == "home":
    import pages.home as home
    home.render()
elif page == "search":
    import pages.search as search
    search.render()
elif page == "about":
    import pages.about as about
    about.render()
elif page == "detail":
    import pages.detail as detail
    detail.render()