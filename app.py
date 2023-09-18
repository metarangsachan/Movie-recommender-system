import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(m_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8662826ff6e72eb2f4f9eec30167b279&language=en-US'.format(m_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/original" + data['poster_path']


def recommend(movie):
    m_index = m[m['title'] == movie].index[0]
    distances = simi[m_index]
    m_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended = []
    recommended_posters = []
    for it in m_list:
        m_id = m.iloc[it[0]].movie_id
        # fetch poster
        recommended.append(m.iloc[it[0]].title)
        recommended_posters.append(fetch_poster(m_id))
        return recommended, recommended_posters


m_dict = pickle.load(open('movies_dict.pkl', 'rb'))
m = pd.DataFrame(m_dict)

simi = pickle.load(open('simi.pkl', 'rb'))

st.title('MOVIE RECOMMENDER SYSTEM')

selected = st.selectbox(
    'How would you like to be contacted?',
    m['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
