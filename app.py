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

def create_df(results, result_type):
    if results and result_type in results:
        data = results[result_type]
        if data:
            df = pd.json_normalize(data)
            #df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x) #Remove extra whitespace but does not work on nested objects.
            return(df)
        else:
            st.warning(f"No {result_type} found.")
    else:
        st.warning(f"No {result_type} found.")

def populate_df(type, media_name):
    search_url = f"{base_url}{type}/"
    params = {f'query': {media_name}, 'fmt': 'json'}
    results = make_request(search_url, params)
    df = create_df(results, f'{type}s')
    return(df)

def display_two_tables(df):
    st.subheader("Interactive data table ")
    st.dataframe(df)

    enable_table = st.checkbox('Do you want a static table?')
    st.caption("(A static table includes expanded nested objects)")
    if enable_table:
        st.subheader("Static table of the data")
        st.table(df)

def gen_score_chart(df):
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

def search_artist(artist_name, selected_tab):
    type = "artist"
    if selected_tab == "Raw MusicBrainz API Data":
        df = populate_df(type, artist_name)

        display_two_tables(df)

    elif selected_tab == "Search Effectiveness Bar Chart":
        df = populate_df(type, artist_name)

        gen_score_chart(df)

def search_album(album_name, selected_tab):
    type = "release"
    if selected_tab == "Raw MusicBrainz API Data":
        df = populate_df(type, album_name)

        display_two_tables(df)

    elif selected_tab == "Search Effectiveness Bar Chart":
        df = populate_df(type, album_name)

        gen_score_chart(df)

def search_song(song_name, selected_tab):
    type = "recording"
    if selected_tab == "Raw MusicBrainz API Data":
        df = populate_df(type, song_name)

        display_two_tables(df)

    elif selected_tab == "Search Effectiveness Bar Chart":
        df = populate_df(type, song_name)

        gen_score_chart(df)

    elif selected_tab == "Length of songs":
        # Add logic for filtered data
        pass

def main():
    st.title("ParaMusic")
    search_query = st.text_input("Enter a song, album, or artist name")
    search_type = st.selectbox("Search Type", ["Song", "Album", "Artist"])

    st.sidebar.subheader("Search Options")
    selected_tab = st.sidebar.radio("Select Tab", ["Filtered Data", "Raw MusicBrainz API Data", "Search Effectiveness Bar Chart"])
    search = st.button("Search") #The button is just for design so users feel comfortable and know the next steps after inputting text.

    if (selected_tab == "Raw MusicBrainz API Data" or selected_tab ==  "Search Effectiveness Bar Chart"):
        if search_query: # It is faster to detect if there is any text_input. The submit button ensures they click out of the text box
            if search_type == "Artist":
                search_artist(search_query, selected_tab)
            elif search_type == "Album":
                search_album(search_query, selected_tab)
            elif search_type == "Song":
                search_song(search_query, selected_tab)

    df = pd.DataFrame()
    if (selected_tab == "Filtered Data"):
        if search_query: # It is faster to detect if there is any text_input. The submit button ensures they click out of the text box
            if search_type == "Artist":
                df = populate_df('artist', search_query)
            elif search_type == "Album":
                df = populate_df('release', search_query)
            elif search_type == "Song":
                df = populate_df('recording', search_query)


        selected_options = st.multiselect('Select Columns to be Displayed', options=df.columns)

        # Filter the dataframe based on the selected options
        filtered_df = df[selected_options]

        if selected_options:
            display_two_tables(filtered_df)

main()
