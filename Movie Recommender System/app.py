import streamlit as st
import pickle                 
import requests                                                #Libraries Used              

movies = pickle.load(open("movies_list.pkl", 'rb')) 
similarity = pickle.load(open("similarity.pkl", 'rb'))         #This is Calculating Similarities Between Movies using ML
movies_list=movies['title'].values                             #Load Pickled Movie Data

st.header("Movie Recommender System [ML]")
selectvalue=st.selectbox("Select movies from Dropdown", movies_list)

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=5cd699e594d617ac2f052c61f3d734a5&language=en-US".format(movie_id)
    data=requests.get(url)
    data=data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/"+poster_path #Loads posters through 'Postman' provided by TMDB 
    return full_path

def recommend(movie):
    index=movies[movies['title']==movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector:vector[1]) #Sorting Movie Matrix
    recommend_movie=[]
    recommend_poster=[]
    for i in distance[1:6]:
        movies_id=movies.iloc[i[0]].id
        recommend_movie.append(movies.iloc[i[0]].title)       #Append(Joining) Movie with Title
        recommend_poster.append(fetch_poster(movies_id))      #Append(Joining) Posters with Movie-ID
    return recommend_movie, recommend_poster                  #Final recommendation



if st.button("Show Recommend"):
    movie_name, movie_poster = recommend(selectvalue)
    col1,col2,col3,col4,col5=st.columns(5)                    #5 movies sorted
    with col1:
        st.text(movie_name[0])                             
        st.image(movie_poster[0])                             #Movie no 1
    with col2:
        st.text(movie_name[1])
        st.image(movie_poster[1])                             #Movie no 2
    with col3:
        st.text(movie_name[2])
        st.image(movie_poster[2])                             #Movie no 3
    with col4:
        st.text(movie_name[3]) 
        st.image(movie_poster[3])                             #Movie no 4
    with col5:
        st.text(movie_name[4]) 
        st.image(movie_poster[4])                             #Movie no 5
