import requests
import streamlit as st

base_url = "https://musicbrainz.org/ws/2/"
def search_artist(artist_name):
    search_url = f"{base_url}artist/"

    # Set up parameters for the request
    params = {
        'query': artist_name,
        'fmt': 'json'  # Requesting the response in JSON format
    }

    # Make the request
    response = requests.get(search_url, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Extract relevant information
        if 'artists' in data:
            artists = data['artists']
            for artist in artists:
                st.write(f"Name: {artist['name']}, ID: {artist['id']}")
        else:
            st.write("No artists found.")
    else:
        st.write(f"Error: {response.status_code}")

def search_album(album_name):
    search_url = f"{base_url}release/"

    # Set up parameters for the request
    params = {
        'query': album_name,
        'fmt': 'json'  # Requesting the response in JSON format
    }

    # Make the request
    response = requests.get(search_url, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Extract relevant information
        if 'releases' in data:
            albums = data['releases']
            for album in albums:
                st.write(f"Name: {album['title']}, Artist: {album['artist-credit']}, ID: {album['id']}")
        else:
            st.write("No artists found.")
    else:
        st.write(f"Error: {response.status_code}")

def search_song(song_name):
    search_url = f"{base_url}recording/"

    # Set up parameters for the request
    params = {
        'query': song_name,
        'fmt': 'json'  # Requesting the response in JSON format
    }

    # Make the request
    response = requests.get(search_url, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Extract relevant information
        if 'recordings' in data:
            songs = data['recordings']
            for song in songs:
                st.write(f"Name: {song['title']}, Artist: {song['artist-credit']}, ID: {song['id']}")
        else:
            st.write("No artists found.")
    else:
        st.write(f"Error: {response.status_code}")

def main():
    st.title("Music Search App")
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

# Example usage
#search_artist("Metallica")
#search_album("Graduation")
#search_song2("No Role Modelz")

#https://coverartarchive.org/release/ID This is a different API tho
