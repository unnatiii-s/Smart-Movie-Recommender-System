import numpy as np
import pandas as pd
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# --- helper functions for data cleaning ---
def convert(text):
    """Extracts names from a stringified list of dictionaries."""
    L = []
    try:
        for i in ast.literal_eval(text):
            L.append(i['name']) 
    except (ValueError, SyntaxError):
        pass
    return L 

def convert3(text):
    """Extracts top 3 names from a stringified list of dictionaries."""
    L = []
    counter = 0
    try:
        for i in ast.literal_eval(text):
            if counter < 3:
                L.append(i['name'])
            counter+=1
    except (ValueError, SyntaxError):
        pass
    return L 

def fetch_director(text):
    """Extracts director name from crew list."""
    L = []
    try:
        for i in ast.literal_eval(text):
            if i['job'] == 'Director':
                L.append(i['name'])
    except (ValueError, SyntaxError):
        pass
    return L 

def collapse(L):
    """Removes spaces from list items (e.g., 'Sam Worthington' -> 'SamWorthington')."""
    L1 = []
    for i in L:
        L1.append(i.replace(" ",""))
    return L1

def recommend(movie, new_df, similarity):
    """
    Recommendation Function:
    Finds the index of the selected movie, retrieves its similarity scores,
    sorts them to find top 5 matches, and prints the titles.
    """
    try:
        index = new_df[new_df['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])
        print(f"Recommendations for {movie}:")
        for i in distances[1:6]:
            print(new_df.iloc[i[0]].title)
    except IndexError:
        print(f"Movie '{movie}' not found.")

def main():
    # 1. Data Collection & Loading
    print("Loading data...")
    movies = pd.read_csv('data/tmdb_5000_movies.csv')
    credits = pd.read_csv('data/tmdb_5000_credits.csv') 

    print("Merging data...")
    movies = movies.merge(credits,on='title')
    # Selecting relevant features
    movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]
    
    # 2. Data Cleaning & Preprocessing
    print("Pre-processing data...")
    movies.dropna(inplace=True)
    
    # Extracting meaningful tags from stringified JSON columns
    movies['genres'] = movies['genres'].apply(convert)
    movies['keywords'] = movies['keywords'].apply(convert)
    movies['cast'] = movies['cast'].apply(convert3)
    movies['crew'] = movies['crew'].apply(fetch_director)
    
    # Text normalization (removing spaces to create unique tags)
    movies['cast'] = movies['cast'].apply(collapse)
    movies['crew'] = movies['crew'].apply(collapse)
    movies['genres'] = movies['genres'].apply(collapse)
    movies['keywords'] = movies['keywords'].apply(collapse)
    
    movies['overview'] = movies['overview'].apply(lambda x:x.split())
    
    # Concatenating all tags into a single 'tags' column
    movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']
    
    new = movies.drop(columns=['overview','genres','keywords','cast','crew'])
    new['tags'] = new['tags'].apply(lambda x: " ".join(x))
    
    # 3. Vectorization (NLP)
    print("Vectorizing...")
    # Using Bag of Words (CountVectorizer) to convert text to vectors
    cv = CountVectorizer(max_features=5000,stop_words='english')
    vector = cv.fit_transform(new['tags']).toarray()
    
    # 4. Similarity Computation
    print("Calculating similarity...")
    # Computing Cosine Similarity between all movie vectors
    similarity = cosine_similarity(vector)
    
    # 5. Testing the Model
    print("Generating recommendations...")
    recommend('Gandhi', new, similarity)
    
    # 6. Saving the Model
    print("Saving models...")
    pickle.dump(new, open('movie_list.pkl','wb'))
    pickle.dump(similarity, open('similarity.pkl','wb'))
    print("Done.")

if __name__ == "__main__":
    main()
