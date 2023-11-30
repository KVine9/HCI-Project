import requests
import pandas as pd
import streamlit as st
import plotly.express as px

base_url = "https://musicbrainz.org/ws/2/"

def make_request(search_url, params):
    response = requests.get(search_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error: {response.status_code}")
        return None

def produce_dataframe(results, result_type):
    if results and result_type in results:
        data = results[result_type]
        if data:
            df = pd.DataFrame(data)
            df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
            return(df)
        else:
            st.warning(f"No {result_type}s found.")
    else:
        st.warning(f"No {result_type}s found.")

def search_artist(artist_name, selected_tab):
    if selected_tab == "Raw MusicBrainz API Data":
        search_url = f"{base_url}artist/"
        params = {'query': artist_name, 'fmt': 'json'}
        results = make_request(search_url, params)
        df = produce_dataframe(results, 'artists')
        st.table(df)
        st.success("Thank you for using ParaMusic")

    elif selected_tab == "Search Effectiveness Bar Chart":
        search_url = f"{base_url}artist/"
        params = {'query': artist_name, 'fmt': 'json'}
        results = make_request(search_url, params)
        df = produce_dataframe(results, 'artists')

        # Extract the "score" values
        scores = df['score']

        # Create a table with the scores
        table_data = {'Index': range(0, len(scores)), 'Score (in %)': scores}
        score_table = pd.DataFrame(table_data)

        # Create a bar table
        fig = px.bar(score_table, x="Index", y="Score (in %)")
        st.subheader("Effectiveness Bar Chart")
        st.plotly_chart(fig)
        st.caption("How effective the search result is to the desired term")

    elif selected_tab == "Filtered Data":
        # We need the logic for this

    elif selected_tab == "Song Lengths":
        st.warning("Please select 'songs' as the search type to get song lengths")

def search_album(album_name, selected_tab):
    if selected_tab == "Raw MusicBrainz API Data":
        search_url = f"{base_url}release/"
        params = {'query': album_name, 'fmt': 'json'}
        results = make_request(search_url, params)
        df = produce_dataframe(results, 'releases')
        st.table(df)
        st.success("Here are the results for your search")

    elif selected_tab == "Search Effectiveness Bar Chart":
        search_url = f"{base_url}artist/"
        params = {'query': album_name, 'fmt': 'json'}
        results = make_request(search_url, params)
        df = produce_dataframe(results, 'artists')

        # Extract the "score" values
        scores = df['score']

        # Create a table with the scores
        table_data = {'Index': range(0, len(scores)), 'Score (in %)': scores}
        score_table = pd.DataFrame(table_data)

        # Create a bar table
        fig = px.bar(score_table, x="Index", y="Score (in %)")
        st.subheader("Effectiveness Bar Chart")
        st.plotly_chart(fig)
        st.caption("How effective the search result is to the desired term")

    elif selected_tab == "Filtered Data":
        # We need logic for filtered data

    elif selected_tab == "song lengths":
        st.warning("Please select 'songs' as the search type to get song lengths")
        

def search_song(song_name, selected_tab):
    if selected_tab == "Raw MusicBrainz API Data":
        search_url = f"{base_url}recording/"
        params = {'query': song_name, 'fmt': 'json'}
        results = make_request(search_url, params)
        df = produce_dataframe(results, 'recordings')
        st.table(df)

    elif selected_tab == "Search Effectiveness Bar Chart":
        search_url = f"{base_url}artist/"
        params = {'query': song_name, 'fmt': 'json'}
        results = make_request(search_url, params)
        df = produce_dataframe(results, 'artists')

        # Extract the "score" values
        scores = df['score']

        # Create a table with the scores
        table_data = {'Index': range(0, len(scores)), 'Score (in %)': scores}
        score_table = pd.DataFrame(table_data)

        # Create a bar table
        fig = px.bar(score_table, x="Index", y="Score (in %)")
        st.subheader("Effectiveness Bar Chart")
        st.plotly_chart(fig)
        st.caption("How effective the search result is to the desired term")

    elif selected_tab == "Filtered Data":
        # Add logic for filtered Data
        pass
    elif selected_tab == "song lengths":
        #Logic is not working for this: Can anyone help in figuring it out?
        search_url = f"{base_url}recording/"
        params = {'query': song_name, 'fmt': 'json'}
        results = make_request(search_url, params)
        df = produce_dataframe(results, 'recordings')

        if df is not None:
            # Extract the "length" values
            lengths = df['length']

            # Create a scatterplot of song lengths
            fig = px.scatter(x=range(len(lengths)), y=lengths, labels={'x': 'Entry Number', 'y': 'Song Length'})
            st.subheader("Song Length (In Milliseconds Scatterplot")
            st.plotly_chart(fig)
        else:
            st.warning("No data available for the selected song.")

def main():
    st.title("ParaMusic")
    search_query = st.text_input("Enter a song, album, or artist name")
    search_type = st.selectbox("Search Type", ["Song", "Album", "Artist"])

    st.sidebar.subheader("Search Options")
    selected_tab = st.sidebar.radio("Select Tab", ["Raw MusicBrainz API Data", "Filtered Data", "Artist Information", "Search Effectiveness Bar Chart"])

    if search_type == "Artist":
        artist_default = st.checkbox('Do you want to search for the current Number 1 Artist Globally: Taylor Swift?')
        if artist_default:
            search_artist("Taylor Swift", selected_tab) 
            
    if st.button("Search"):
        if search_type == "Artist":
            search_artist(search_query, selected_tab)
        elif search_type == "Album":
            search_album(search_query, selected_tab)
        elif search_type == "Song":
            search_song(search_query, selected_tab)


main()
