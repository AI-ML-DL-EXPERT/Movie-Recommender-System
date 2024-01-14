import pandas as pd
import pickle
import streamlit as st
import requests


def fetch_poster(movie_id):
    response = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=bf1f8b1d99caa2d6c15fb0d3fcacd643&language=en-US")
    data = response.json()

    return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]


def recommend(movie):
    index = movies[movies["title"] == movie].index[0]
    movies_list = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])[1: 6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters


movies_dict = pickle.load(open("movies_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open("similarity.pkl", "rb"))

st.title("Movie Recommender System")

selected_movie_name = st.selectbox(
    "List of Movies:- ",
    movies["title"].values
)

if st.button("Recommend"):
    names, poster = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(poster[0])

    with col2:
        st.text(names[1])
        st.image(poster[1])

    with col3:
        st.text(names[2])
        st.image(poster[2])

    with col4:
        st.text(names[3])
        st.image(poster[3])

    with col5:
        st.text(names[4])
        st.image(poster[4])
