# **Project Report: Smart Movie Recommender System**

**Submitted by:** Tarun Nagar

---

## **1. Abstract**
The Smart Movie Recommender System is an advanced web-based application designed to solve the problem of information overload in digital entertainment. By leveraging Content-Based Filtering and Natural Language Processing (NLP), the system analyzes movie metadata—including genres, keywords, cast, and crew—to provide personalized recommendations. This report details the development of an end-to-end system that encompasses data preprocessing, vectorization, similarity computation, and deployment via a Streamlit interface. The result is a robust, interactive platform that enhances user experience by accurately predicting and suggesting movies similar to a user's preference.

---

## **2. Introduction**
In the era of streaming services like Netflix and Prime Video, users are overwhelmed with choices. A recommendation system filters this vast amount of information to provide relevant content. This project focuses on building a **Content-Based Recommendation System**. Unlike Collaborative Filtering, which relies on user interaction history (ratings/clicks), this system relies on the intrinsic properties of the movies themselves. By analyzing the textual features of a movie, we can mathematically compute similarity scores and recommend the closest matches.

---

## **3. Problem Statement**
Users often spend more time searching for a movie than watching it. Existing platforms can feel impersonal or overwhelming. The objective of this project is to build a simplified, highly accurate engine that suggests movies based on a specific input movie, ensuring that the recommendations are thematically and contextually relevant. The challenge lies in converting unstructured text data (plots, cast lists) into structured numerical vectors that a machine can analyze.

---

## **4. Methodology**
The development process followed a structured data science pipeline:

### **4.1. Data Collection**
We utilized the **TMDB 5000 Movie Dataset**, which includes two main files:
- `tmdb_5000_movies.csv`: Contains metadata like budget, genres, homepage, id, keywords, original_language, original_title, overview, popularity, production_companies, release_date, revenue, runtime, status, tagline, title, vote_average, vote_count.
- `tmdb_5000_credits.csv`: Contains movie_id, title, cast, and crew.

### **4.2. Data Preprocessing**
The raw data contained JSON-formatted columns. We implemented Python functions to parse these columns into usable lists of strings.
- **Merged** the two datasets on the 'title' column.
- **Extracted** meaningful tags from `genres`, `keywords`, `cast` (top 3 actors), and `crew` (director).
- **Cleaned** the text by removing spaces to create unique tokens (e.g., 'Sam Worthington' becomes 'SamWorthington' to distinguish it from another 'Sam').

### **4.3. Feature Engineering**
We created a new column called `tags` by concatenating the `overview`, `genres`, `keywords`, `cast`, and `crew`. This single text blob represents the essence of the movie.

### **4.4. Vectorization (NLP)**
We employed the **Bag-of-Words** technique using Scikit-Learn's `CountVectorizer`. We converted the text tags into numerical vectors, limiting the vocabulary to the top 5000 frequent words to reduce dimensionality (`max_features=5000`) and removing common English stop words.

### **4.5. Similarity Computation**
We calculated the **Cosine Similarity** between all 4806 movie vectors.
\[ \text{Cosine Similarity} (A, B) = \frac{A \cdot B}{\|A\| \|B\|} \]
This resulted in a similarity matrix of size 4806x4806, where each value represents the closeness of two movies.

### **4.6. Deployment**
The model (data frame and similarity matrix) was serialized using `pickle` and integrated into a **Streamlit** web application.

---

## **5. System Architecture**
The system follows a client-server architecture:

- **Frontend**: Built with **Streamlit**, providing an interactive dashboard. It includes:
  - A comprehensive visual design with a custom Dark Theme.
  - A Dropdown menu for movie selection.
  - A Recommendation Grid displaying posters and titles.
- **Backend**: Python scripts handle the logic.
  - `run_notebook.py`: Performs offline training and generates `.pkl` files.
  - `app.py`: Loads the model into memory to serve real-time requests.
- **API Integration**: The app fetches real-time movie posters using the **TMDB API** via HTTP requests.

---

## **6. Results**
The system successfully recommends movies with high contextual relevance.
- **Input**: "Avatar"
- **Output**: "Aliens", "Guardians of the Galaxy", "Star Trek", "Star Trek Into Darkness", "Moonraker".
- **Performance**: The response time for generating recommendations is near-instantaneous (< 1 second) as the pre-computed similarity matrix allows for O(1) lookups.
- **UI/UX**: The application features a "Premium Dark UI" with red accents, ensuring a professional look and feel.

---

## **7. Conclusion**
The Smart Movie Recommender System successfully demonstrates the power of NLP and Content-Based Filtering. It provides a seamless user experience, bridging the gap between raw data and actionable insights. The project covers the full lifecycle of a machine learning application, from raw data cleaning to a deployed web product.

---

## **8. Future Scope**
- **Hybrid Approach**: Integrating collaborative filtering (user ratings) to improve accuracy.
- **Sentiment Analysis**: Analyzing user reviews to refine recommendations further.
- **Real-time Learning**: Updating the model as new movies are released without full retraining.
- **Mobile App**: Porting the interface to a mobile-native framework like React Native.

---

## **9. References**
1. TMDB 5000 Movie Dataset - Kaggle.
2. Scikit-Learn Documentation - Feature Extraction & Pairwise Metrics.
3. Streamlit Documentation - Layouts and Theming.
4. Python 3.9 Documentation.
