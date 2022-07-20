#importing packages
import streamlit as st
import pickle
import pandas as pd
import requests

#render title
st.title('Movie Recommender System')

#loading from pickle
movies = pickle.load(open('new_movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

#util functions
def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/'+str(movie_id)+'?api_key=cbd978ec041c63cf0296b9196237cda2&language=en-US')
    data = response.json()
    return 'https://image.tmdb.org/t/p/w500/'+data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title']==movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse = True, key = lambda x : x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []
    for film in movies_list:
        recommended_movies.append(movies.iloc[film[0]].title)
        #fetch poster from API 
        recommended_movies_posters.append(fetch_poster(movies.iloc[film[0]].movie_id))
    return recommended_movies, recommended_movies_posters

#selectbox
selected_movie_name = st.selectbox(
    'Enter movie name ',
    movies['title'].values
)

#button
if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    #rendering 5 posters
    cols = st.columns(5)
    for itm in range(5):
        with cols[itm]:
            st.text(names[itm])
            st.image(posters[itm])