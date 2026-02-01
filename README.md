# Smart Movie Recommender System

The **Smart Movie Recommender System** is an end-to-end AI/ML based web application designed with a **Premium Dark UI**. It recommends similar movies to users based on their preferences using Content-Based Filtering techniques.

The project involves parsing a public movie dataset (TMDB), extracting rich text features (overview, genres, keywords, cast, crew) using NLP, and computing movie similarity via Cosine Similarity. The final model is deployed on a sleek Streamlit web interface that features a minimalist design, custom styling, and interactive elements.

## ✨ Features
-   **Content-Based Filtering**: Accurate recommendations based on movie metadata.
-   **Premium Dark UI**: A professional dark theme with vibrant accents (`#E50914`) and minimalist design.
-   **Interactive Interface**: Custom styled dropdowns, buttons, and hover effects.
-   **Poster Integration**: Fetches real-time high-quality movie posters via the TMDB API.
-   **Responsive Layout**: Optimized for wide screens with perfect alignment.

## 🛠️ Tech Stack
-   **Python**: Core logic.
-   **Pandas & NumPy**: Data manipulation.
-   **Scikit-Learn**: Vectorization and Similarity computation.
-   **Streamlit**: Web framework (with custom CSS injection).
-   **TMDB API**: Movie assets.

## 🚀 Setup & Installation

1.  **Clone the repository** (if applicable) or download the files.
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Generate the Model**:
    Run the preprocessing script to generate `movie_list.pkl` and `similarity.pkl`.
    ```bash
    python run_notebook.py
    ```
4.  **Run the App**:
    ```bash
    streamlit run app.py
    ```

## 📂 Project Structure
-   `app.py`: The main Streamlit application with custom UI logic.
-   `run_notebook.py`: Script to process data and train the model.
-   `data/`: Folder containing the TMDB dataset (`tmdb_5000_movies.csv`, `tmdb_5000_credits.csv`).
-   `requirements.txt`: Python dependencies.
-   `movie_list.pkl` & `similarity.pkl`: Generated model files.

## 👥 Usage
-   Launch the app.
-   Select a movie from the styled dropdown menu.
-   Click "Show Recommendations".
-   Enjoy the curated list of similar movies displayed with their official posters.

---
**Developed by Tarun Nagar**
