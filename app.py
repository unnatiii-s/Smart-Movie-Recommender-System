import pickle
import streamlit as st
import requests

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart Movie Recommender",
    layout="wide"
)

# ---------------- LIGHT MODERN UI ----------------
st.markdown("""
<style>

/* Root App */
.stApp {
    background: linear-gradient(120deg, #f8f9fa, #eef1f5);
    color: #1a1a1a;
    font-family: 'Segoe UI', sans-serif;
}
#MainMenu, footer, header {visibility: hidden;}

/* Headings */
h1 {
    text-align: center;
    font-weight: 800;
    color: #1f4fd8;
    letter-spacing: 1px;
}
h3 {
    color: #1f4fd8;
}

/* About Button */
.about-btn button {
    background: #ffffff;
    border: 1px solid #cfd6e0;
    color: #1f4fd8;
    font-weight: 700;
    border-radius: 8px;
}
.about-btn button:hover {
    background: #1f4fd8;
    color: #ffffff;
}

/* Selectbox */
.stSelectbox > div {
    background: #ffffff;
    border-radius: 8px;
    border: 1px solid #cfd6e0;
}
.stSelectbox label {
    color: #1f4fd8 !important;
    font-weight: 600;
}

/* Button */
.stButton > button {
    background: #1f4fd8;
    color: #ffffff;
    font-weight: 700;
    border-radius: 8px;
    height: 3em;
    border: none;
    transition: all 0.25s ease;
}
.stButton > button:hover {
    background: #163db7;
    transform: translateY(-2px);
}

/* Movie Card */
.movie-container {
    background: #ffffff;
    border: 1px solid #e1e6ef;
    border-radius: 14px;
    padding: 10px;
    text-align: center;
    transition: all 0.3s ease;
}
.movie-container:hover {
    transform: translateY(-6px);
    box-shadow: 0 10px 25px rgba(0,0,0,0.12);
}
.movie-title {
    margin-top: 8px;
    font-size: 14px;
    font-weight: 600;
    color: #1a1a1a;
}
img { border-radius: 14px; }

/* Info Cards */
.info-card {
    background: #ffffff;
    border: 1px solid #e1e6ef;
    border-radius: 16px;
    padding: 30px;
    margin-bottom: 25px;
}
.info-text {
    font-size: 16px;
    line-height: 1.8;
    color: #333333;
}
.highlight {
    color: #1f4fd8;
    font-weight: 700;
}

/* Welcome */
.welcome {
    text-align: center;
    font-size: 17px;
    color: #444444;
    margin: 15px 0 25px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HELPER FUNCTIONS ----------------
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    try:
        data = requests.get(url).json()
        poster_path = data.get("poster_path")

        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster"
    except:
        return "https://via.placeholder.com/500x750?text=No+Poster"

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )
    names, posters = [], []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        names.append(movies.iloc[i[0]].title)
        posters.append(fetch_poster(movie_id))
    return names, posters

# ---------------- PAGE STATE ----------------
if "page" not in st.session_state:
    st.session_state.page = "Home"

# ---------------- TOP RIGHT ABOUT BUTTON ----------------
spacer, about_col = st.columns([8, 1])
with about_col:
    st.markdown('<div class="about-btn">', unsafe_allow_html=True)
    if st.button("ℹ️ About"):
        st.session_state.page = "About"
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- MAIN TITLE ----------------
st.title("🎬 Smart Movie Recommender")

# ---------------- HOME PAGE ----------------
if st.session_state.page == "Home":
    try:
        movies = pickle.load(open("movie_list.pkl", "rb"))
        similarity = pickle.load(open("similarity.pkl", "rb"))
        movie_list = movies["title"].values
    except:
        st.error("Model files not found. Please train the model first.")
        st.stop()

    st.markdown("<div class='welcome'>Select one movie and get instant recommendations 🎥</div>", unsafe_allow_html=True)

    # Centered small search bar with placeholder
    left, center, right = st.columns([1, 2, 1])
    with center:
        selected_movie = st.selectbox(
            "Search Movie",
            movie_list,
            index=None,
            placeholder="Select a movie..."
        )
        show = st.button("Recommend")

    if show:
        if selected_movie is None:
            st.warning("Please select a movie first.")
        else:
            with st.spinner("Finding similar movies..."):
                names, posters = recommend(selected_movie)
                c1, c2, c3, c4, c5 = st.columns(5)

                def display(name, poster, col):
                    with col:
                        st.markdown(
                            f"<div class='movie-container'><div class='movie-title'>{name}</div></div>",
                            unsafe_allow_html=True
                        )
                        st.image(poster, use_container_width=True)

                display(names[0], posters[0], c1)
                display(names[1], posters[1], c2)
                display(names[2], posters[2], c3)
                display(names[3], posters[3], c4)
                display(names[4], posters[4], c5)

# ---------------- ABOUT PAGE ----------------
elif st.session_state.page == "About":
    st.markdown("""
    <div class="info-card">
        <h3>🧠 How It Works</h3>
        <p class="info-text">
            The <span class="highlight">Smart Movie Recommender System</span>
            analyzes movie descriptions, genres, keywords, cast, and crew to
            identify similarities between movies.
        </p>
        <p class="info-text">
            These features are converted into numerical form and compared
            using <span class="highlight">Cosine Similarity</span> to generate
            relevant movie recommendations.
        </p>
    </div>

    <div class="info-card">
        <h3>👨‍💻 Developer</h3>
        <p class="info-text">
            Developed by <span class="highlight">Unnati Sutradhar</span>
        </p>
        <p class="info-text">
            A clean, modern, and efficient movie recommendation system
            designed for academic and real-world applications.
        </p>
    </div>
    """, unsafe_allow_html=True)
