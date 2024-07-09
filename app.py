import pickle
import streamlit as st
import requests
from sklearn.metrics.pairwise import cosine_similarity


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    # Get the vector representation for the input movie
    input_vector = movies[movies['title'] == movie]['vectorized_tags'].values[0]

    # Calculate cosine similarity between the input movie and all other movies
    similarities = cosine_similarity([input_vector], list(movies['vectorized_tags']))

    # Get the indices of the most similar movies
    similar_indices = similarities.argsort()[0][-6:-1][::-1]

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in similar_indices:
        # Fetch the movie poster
        movie_id = movies.iloc[i].movie_id  # Assuming you have a 'movie_id' column in your DataFrame
        recommended_movie_posters.append(fetch_poster(movie_id))  # You need to define the 'fetch_poster' function
        recommended_movie_names.append(movies.iloc[i].title)

    return recommended_movie_names, recommended_movie_posters


hidden = """
    <style>

    footer {visibility: hidden;}
       
    </style>
    """

st.markdown(hidden,unsafe_allow_html=True)

st.header('Movie Recommending System')
movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarities.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a Movie",
    movie_list
)

if st.button('Recommend Movies'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.markdown(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.markdown(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.markdown(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.markdown(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])


st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
st.markdown("Team Members: <br>Umaid Shaan <br> Abhay Suresh <br> Abhyuday Choumal", unsafe_allow_html=True)