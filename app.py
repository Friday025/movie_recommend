import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=ad26761976d9d5350a28f9c8215cd871")
    data = response.json() 
    if 'poster_path' in data:
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    else:
        return "URL_to_a_default_image_or_placeholder"  # Provide a default image URL

# Load movies and similarity matrix
movies_dict = pickle.load(open("movies_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open("similarity.pkl", "rb"))

movies.reset_index(drop=True, inplace=True)


def recommend(movie):
    movie_index = movies[movies['original_title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].id  # Ensure your DataFrame has the correct TMDb ID
        recommended_movies.append(movies.iloc[i[0]].original_title)
        recommended_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_posters

# Streamlit application
st.title("Movie Recommendations System")

# Select box for movie selection
select_movie = st.selectbox("Which movie would you like to recommend?", movies['original_title'].values)
if st.button("Recommend"):
    recommended_names, recommended_posters = recommend(select_movie)

    # Display recommended movies and posters in a 5-column grid
    cols = st.columns(5)  # Create 5 columns
    for idx, (name, poster_url) in enumerate(zip(recommended_names, recommended_posters)):
        with cols[idx % 5]:
            st.image(poster_url, use_column_width=True)
            st.write(name) 