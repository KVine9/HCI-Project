import requests
import streamlit as st


base_url = "https://musicbrainz.org/ws/2/"

def make_request(search_url, params):
    response = requests.get(search_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error: {response.status_code}")
        return None

def display_results(results, result_type):
    if results and result_type in results:
        data = results[result_type]
        if data:
            st.table(data)
        else:
            st.warning(f"No {result_type}s found.")
    else:
        st.warning(f"No {result_type}s found.")

def search_artist(artist_name):
    st.sidebar.subheader("Search Options")
    selected_tab = st.sidebar.radio("Select Tab", ["Raw MusicBrainz API data", "Filtered Data", "Artist Information"])

    if selected_tab == "Raw MusicBrainz API data":
        search_url = f"{base_url}artist/"
        params = {'query': artist_name, 'fmt': 'json'}
        results = make_request(search_url, params)
        display_results(results, 'artists')
    elif selected_tab == "Filtered Data":
        # Add logic for filtered data
        pass
    elif selected_tab == "Artist Information":
        # Add logic for artist information
        pass

def search_album(album_name):
    st.sidebar.subheader("Search options")
    selected_tab = st.sidebar.radio("Select Tab", ["Raw MusicBrainz API Data", "Filtered Data", "Release Events"])

    if selected_tab == "Raw MusicBrainz API Data":
        search_url = f"{base_url}release/"
        params = {'query': album_name, 'fmt': 'json'}
        results = make_request(search_url, params)
        display_results(results, 'releases')
    elif selected_tab == "Filtered Data":
        # Add logic for filtered Data
        pass
    elif selected_tab == "Release Events":
        # Add logic for filtered data
        pass

def search_song(song_name):
    st.sidebar.subheader("Search options")
    selected_tab = st.sidebar.radio("Select Tab", ["Raw MusicBrainz API Data", "Filtered Data", "Length of songs"])

    if selected_tab == "Raw MusicBrainz API Data":
        search_url = f"{base_url}recording/"
        params = {'query': song_name, 'fmt': 'json'}
        results = make_request(search_url, params)
        display_results(results, 'recordings')
    elif selected_tab == "Filtered Data":
        # Add logic for filtered Data
        pass
    elif selected_tab == "Length of songs":
        # Add logic for filtered data
        pass

def main():
    st.title("Music Search App")
    st.markdown("<title style = 'text-align': center; 'color': blue; '>Music Search App </title>", unsafe_allow_html=True)
    search_query = st.text_input("Enter a song, album, or artist name")
    search_type = st.selectbox("Search Type", ["Song", "Album", "Artist"])

    if st.button("Search"):
        if search_type == "Artist":
            search_artist(search_query)
        elif search_type == "Album":
            search_album(search_query)
        elif search_type == "Song":
            search_song(search_query)

main()
