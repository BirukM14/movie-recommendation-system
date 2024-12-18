import streamlit as st
import pickle

# Load data
movies = pickle.load(open("movies_list.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

movies_list = movies["title"].values

# Streamlit UI
st.header("Movie Recommender System")
selectvalue = st.selectbox("Select a movie from the dropdown:", movies_list)


def recommend(movie):
    # Check if the movie exists
    if movie not in movies["title"].values:
        st.error("Movie not found in the dataset!")
        return []
    
    # Get index of the selected movie
    index = movies[movies["title"] == movie].index[0]
    
    # Check if index exists in similarity matrix
    if index >= len(similarity):
        st.error("Similarity index out of range!")
        return []
    
    # Calculate distances and sort recommendations
    distances = sorted(
        list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1]
    )
    recommend_movie = []
    
    # Append top 5 recommendations (skip the first one, which is itself)
    for i in distances[1:6]:
        recommend_movie.append(movies.iloc[i[0]].title)
    return recommend_movie


if st.button("Show Recommendation"):
    movie_name = recommend(selectvalue)
    if movie_name:  # Ensure recommendations are valid
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.text(movie_name[0])
        with col2:
            st.text(movie_name[1])
        with col3:
            st.text(movie_name[2])
        with col4:
            st.text(movie_name[3])
        with col5:
            st.text(movie_name[4])
    else:
        st.error("No recommendations available!")
