🎬 Content-Based Movie Recommendation System

Project Overview:
This is a content-based movie recommendation system built with Python and Streamlit. It suggests movies similar to a selected movie by comparing movie features such as genre, keywords, cast, and crew. Recommendations are generated using a precomputed similarity matrix based on these metadata features, and the app displays the top 5 recommended movies along with their posters in a clean and interactive web interface.

✨ Key Features
Content-based recommendations using movie metadata (genre, keywords, cast, crew)
Interactive and responsive UI using Streamlit
Dynamic poster retrieval from The Movie Database (TMDB) API
Fast recommendations using cosine similarity and precomputed similarity matrix
Easy to use: just select a movie and get recommendations

🖥️ Demo / Screenshots
⚡ Challenges Faced
Feature Engineering: Combining genre, keywords, cast, and crew into a single feature set for similarity calculation was challenging.
Data Cleaning: Handling missing or inconsistent metadata (e.g., missing cast info or keywords) required careful preprocessing.
Poster Fetching: Ensuring that posters from TMDB API load correctly, even when some movies do not have poster images.
Performance Optimization: Precomputing similarity matrices was necessary to ensure fast recommendations in the app.
