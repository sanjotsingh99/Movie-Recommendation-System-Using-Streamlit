import pickle
import streamlit as st
import json
import urllib
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=1019d1b769928fd362ff4d2c1b9f0e14&language=en-US".format(movie_id)
    raw = urllib.request.urlopen(url)
    json_object = json.load(raw)
    poster_path = json_object['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def fetch_cast_poster(movie_id,movie_cast,movie):
    url="https://api.themoviedb.org/3/movie/{}/credits?api_key=1019d1b769928fd362ff4d2c1b9f0e14&language=en-US".format(movie_id)
    raw = urllib.request.urlopen(url)
    json_raw = raw.readlines()
    json_object = json.loads(json_raw[0])
    movie_func_poster=[]

    for i in json_object['cast']:
                profile_path = str(i['profile_path'])
                full_path = "https://image.tmdb.org/t/p/w500/" + profile_path
                full_path.split(",")
                movie_func_poster.append(full_path)

    return movie_func_poster



def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    selected_movie_poster= []
    movie_cast=[]
    movie_cast_poster=[]
    movie_cast.append(newest_df.iloc[index].cast)
    movie_cast_poster.append(fetch_cast_poster(movies.iloc[index].movie_id,movie_cast,movie))
    selected_movie_poster.append(fetch_poster(movies.iloc[index].movie_id))
    recommended_movie_posters = []
    for i in distances[1:11]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters,selected_movie_poster,movie_cast,movie_cast_poster


st.header('Movie Recommender System')
movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))
newest_df=pickle.load(open('newest_df.pkl','rb'))
reviews = pickle.load(open('reviews.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    st.header(selected_movie)
    recommended_movie_names,recommended_movie_posters,selected_movie_poster,movie_cast,movie_cast_poster = recommend(selected_movie)
    st.image(selected_movie_poster)

    index = newest_df[newest_df['title'] == selected_movie].index[0]
    st.markdown('Title - '+ newest_df.iloc[index].title )
    st.markdown('Overview -  ' + str(newest_df.iloc[index].overview))
    st.markdown('Rating -  ' + str(newest_df.iloc[index].vote_average) + "/10")
    st.markdown('Status -  ' + newest_df.iloc[index].status)
    st.markdown('Genre -  ' + str(newest_df.iloc[index].genres))
    st.markdown('Runtime - '+ str(newest_df.iloc[index].runtime)+" min")
    st.markdown('Director -  ' + str(newest_df.iloc[index].crew))
    st.markdown('Release Date - ' + newest_df.iloc[index].release_date)

        #CAST
    st.header('CAST')
    col_1, col_2, col_3, col_4, col_5 = st.columns(5)
    with col_1:
        st.image(movie_cast_poster[0][0])
        st.markdown(movie_cast[0][0])
    with col_2:
        st.image(movie_cast_poster[0][1])
        st.markdown(movie_cast[0][1])
    with col_3:
        st.image(movie_cast_poster[0][2])
        st.markdown(movie_cast[0][2])
    with col_4:
        st.image(movie_cast_poster[0][3])
        st.markdown(movie_cast[0][3])
    with col_5:
        st.image(movie_cast_poster[0][4])
        st.markdown(movie_cast[0][4])


        #REVIEWS
    st.header('Reviews')
    index = movies[movies['title'] == selected_movie].index[0]
    movie_id=str(movies.iloc[index].movie_id)

    st.markdown("1. "+str(reviews.iloc[index].content[0]))
    st.markdown("2. "+str(reviews.iloc[index].content[1]))


    # Columns for recommendations
    st.subheader('Recommendations for you')
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.image(recommended_movie_posters[0])
        st.markdown(recommended_movie_names[0])
    with col2:
        st.image(recommended_movie_posters[1])
        st.markdown(recommended_movie_names[1])

    with col3:
        st.image(recommended_movie_posters[2])
        st.markdown(recommended_movie_names[2])
    with col4:
        st.image(recommended_movie_posters[3])
        st.markdown(recommended_movie_names[3])
    with col5:
        st.image(recommended_movie_posters[4])
        st.markdown(recommended_movie_names[4])


    col6, col7, col8, col9, col10=st.columns(5)
    with col6:
        st.image(recommended_movie_posters[5])
        st.markdown(recommended_movie_names[5])
    with col7:
        st.image(recommended_movie_posters[6])
        st.markdown(recommended_movie_names[6])

    with col8:
        st.image(recommended_movie_posters[7])
        st.markdown(recommended_movie_names[7])
    with col9:
        st.image(recommended_movie_posters[8])
        st.markdown(recommended_movie_names[8])
    with col10:
        st.image(recommended_movie_posters[9])
        st.markdown(recommended_movie_names[9])




