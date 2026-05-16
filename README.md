
# 🎬 Content-Based Movie Recommendation System

![Front Page](images/machine-learning-project-movie-recommendation-system.webp)

## Project Overview
This is a content-based movie recommendation system built with Python and Streamlit. It suggests movies similar to a selected movie by comparing movie features such as genre, keywords, cast, and crew. Recommendations are generated using a precomputed similarity matrix based on these metadata features, and the app displays the top 5 recommended movies along with their posters in a clean and interactive web interface.

## How This Project Works

### 1) Data and Feature Preparation
- The notebook (`movie_recommended .ipynb`) loads:
  - `Dataset/tmdb_5000_movies.csv`
  - `Dataset/tmdb_5000_credits.csv`
- It merges and cleans data, then builds a combined text representation for each movie using:
  - genres
  - keywords
  - cast
  - crew

### 2) Vectorization and Similarity
- The combined movie text is converted into semantic vectors (using `sentence-transformers`).
- Cosine similarity is computed between every pair of movies.
- Two files are saved for fast app startup:
  - `movie_list.pkl` (processed movie metadata)
  - `similarity.pkl` (precomputed similarity matrix)

### 3) Recommendation Flow in `app.py`
1. User selects a movie title from a Streamlit dropdown.
2. The app finds the selected movie index in `movie_list.pkl`.
3. It reads the corresponding similarity scores from `similarity.pkl`.
4. Movies are sorted by similarity score.
5. The top 5 most similar movies are returned.
6. For each recommendation, poster image is fetched from TMDB API and shown in the UI.

## Key Features
- Content-based recommendations using movie metadata (genre, keywords, cast, crew)
- Interactive and responsive UI using Streamlit
- Dynamic poster retrieval from The Movie Database (TMDB) API
- Fast recommendations using cosine similarity and precomputed similarity matrix
- Easy to use: select a movie and get recommendations instantly

## Project Structure
```text
.
├── app.py
├── movie_recommended .ipynb
├── movie_list.pkl
├── similarity.pkl
├── Dataset/
│   ├── tmdb_5000_movies.csv
│   └── tmdb_5000_credits.csv
├── requirements.txt
└── runtime.txt
```

## Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open the local Streamlit URL (usually `http://localhost:8501`).

### Demo Screenshot ⚡

![Demo Screenshot](images/Screenshot.png)
## Deployment
This Movie Recommendation System project is deployed live using Streamlit, allowing anyone to explore and interact with the app directly from a web browser. Streamlit is a powerful Python framework that makes it easy to create and share beautiful, interactive web applications for data science and machine learning projects.
The application provides a content-based movie recommendation system using genres, keywords, cast, and crew information. Users can input a movie, and the app instantly suggests similar movies along with their posters for a smooth and engaging experience.
You can try the live app here: https://49lgybtk94timewwkj94jk.streamlit.app
## Challenges Faced
Feature Engineering: Combining genre, keywords, cast, and crew into a single feature set for similarity calculation was challenging.
Data Cleaning: Handling missing or inconsistent metadata (e.g., missing cast info or keywords) required careful preprocessing.
Poster Fetching: Ensuring that posters from TMDB API load correctly, even when some movies do not have poster images.
Performance Optimization: Precomputing similarity matrices was necessary to ensure fast recommendations in the app.
Streamlit Deployment: Managing dependency conflicts, ensuring smooth app loading, and making the interface user-friendly.

## Conclusion
This Content-Based Movie Recommendation System demonstrates how combining multiple metadata features into a single tags column and leveraging transformer-based embeddings can create meaningful and accurate movie recommendations. By using cosine similarity, the app delivers fast and relevant suggestions in an interactive interface. The project highlights the importance of data preprocessing, feature integration, and semantic vectorization when building practical machine learning applications.
