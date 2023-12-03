import requests
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu #pip install streamlit_option_menu
from streamlit_extras.stylable_container import stylable_container #pip install streamlit-extras
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
            # df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x) #Remove extra whitespace but does not work on nested objects.
            return (df)
        else:
            st.warning(f"No {result_type} found.")
    else:
        st.warning(f"No {result_type} found.")


def populate_df(type, media_name):
    search_url = f"{base_url}{type}/"
    params = {f'query': {media_name}, 'fmt': 'json'}
    results = make_request(search_url, params)
    df = create_df(results, f'{type}s')
    return (df)


def display_two_tables(df):
    st.subheader("Interactive data table ")
    st.dataframe(df)
    st.success("See your requested interactive table above!")

    enable_table = st.checkbox('Do you want a static table?')
    st.caption("(A static table includes expanded nested objects)")
    if enable_table:
        st.subheader("Static table of the data")
        st.table(df)
        st.success("See your requested static table displaying expanded nested objects above!")

def gen_score_chart(df):
    # Extract the "score" values
    scores = df['score']

    # Create a table with the scores
    table_data = {'Entry Number': range(0, len(scores)), 'Score (in %)': scores}
    score_table = pd.DataFrame(table_data)

    # Create a bar table
    fig = px.bar(score_table, x="Entry Number", y="Score (in %)")
    st.subheader("Effectiveness Bar Chart")
    st.plotly_chart(fig)
    st.caption("How effective the search result is to the desired term")
    st.success("See your requested Search Effectiveness results above!")

def Generate_Scatterplot(df, num_results):
    if df is not None:
        # Extract the "length" values
        lengths = df['length']

        # Create a scatterplot of song lengths
        fig = px.scatter(x=range(num_results), y=lengths[:num_results],
                         labels={'x': 'Entry Number', 'y': 'Song Length'})
        st.subheader(f"Song Length Scatterplot ({num_results} results)")
        st.plotly_chart(fig)
        st.caption(f"Displays the song length for each entry in milliseconds. (Divide the milliseconds by 1000 to get seconds)")
        st.success("See your requested Scatterplot above!")
    else:
        st.warning("No data available for the selected song")

def gen_media_map(df):
    country_coordinates = {
        'US': (37.09024, -95.712891),
        'JP': (36.204824, 138.252924),
        'GB': (55.378051, -3.435973),
        'DE': (51.165691, 10.451526),
        'FR': (46.227638, 2.213749),
        'BE': (50.503887, 4.469936),
        'IT': (41.87194, 12.56738),
        'CA': (56.130366, -106.34677),
        'SE': (60.128161, 18.643501),
        'FI': (61.92411, 25.748151),
        'NL': (52.132633, 5.291266),
        'ES': (40.463667, -3.74922),
        'AU': (-25.274398, 133.77513),
        'RU': (61.52401, 105.318756),
        'BR': (-14.235004, -51.92528),
        'KR': (35.907757, 127.766922),
        'AT': (47.516231, 14.550072),
        'PL': (51.919438, 19.145136),
        'CH': (46.818188, 8.227512),
        'DK': (56.26392, 9.501785),
        'GR': (39.074208, 21.824312),
        'NO': (60.472024, 8.468946),
        'EE': (58.595272, 25.013607),
        'LV': (56.879635, 24.603189),
        'CZ': (49.817492, 15.472962)
    }

    # Create a new DataFrame with country name, latitude, and longitude
    new_df = pd.DataFrame(columns=['country', 'latitude', 'longitude'])

    for country_code in df['country']:
        if country_code in country_coordinates:
            country_name = country_coordinates[country_code]
            latitude, longitude = country_coordinates[country_code]
            new_row = pd.DataFrame([[country_name, latitude, longitude]], columns=['country', 'latitude', 'longitude'])
            new_df = pd.concat([new_df, new_row], ignore_index=True)

    st.subheader("Media Map")
    st.map(new_df)
    st.caption("Shows the different entries' country origin")
    st.success("See your requested Media Map above!")

def search_artist(artist_name, selected_tab):
    type = "artist"

    if (selected_tab == "Filtered Data"):
        df = populate_df(type, artist_name)

        selected_options = st.multiselect('Select Columns to be Displayed', options=df.columns)

        # Filter the dataframe based on the selected options
        filtered_df = df[selected_options]

        if selected_options:
            display_two_tables(filtered_df)

    if selected_tab == "Raw MusicBrainz API Data":
        df = populate_df(type, artist_name)

        display_two_tables(df)

    elif selected_tab == "Display Media Map":
        df = populate_df(type, artist_name)

        gen_media_map(df)

    elif selected_tab == "Search Effectiveness Bar Chart":
        df = populate_df(type, artist_name)

        gen_score_chart(df)
    elif selected_tab == "Song Length Scatterplot":
        st.error("Scatterplot does not work on Artist Names, please set search type to song")

def search_album(album_name, selected_tab):
    type = "release"

    if (selected_tab == "Filtered Data"):
        df = populate_df(type, album_name)

        selected_options = st.multiselect('Select Columns to be Displayed', options=df.columns)

        # Filter the dataframe based on the selected options
        filtered_df = df[selected_options]

        if selected_options:
            display_two_tables(filtered_df)

    if selected_tab == "Raw MusicBrainz API Data":
        df = populate_df(type, album_name)

        display_two_tables(df)

    elif selected_tab == "Display Media Map":
        df = populate_df(type, album_name)

        gen_media_map(df)

    elif selected_tab == "Search Effectiveness Bar Chart":
        df = populate_df(type, album_name)

        gen_score_chart(df)

    elif selected_tab == "Song Length Scatterplot":
        st.error("Scatterplot does not work on Album Names, please set search type to song")

def search_song(song_name, selected_tab):
    type = "recording"

    if (selected_tab == "Filtered Data"):
        df = populate_df(type, song_name)

        selected_options = st.multiselect('Select Columns to be Displayed', options=df.columns)

        # Filter the dataframe based on the selected options
        filtered_df = df[selected_options]

        if selected_options:
            display_two_tables(filtered_df)

    if selected_tab == "Raw MusicBrainz API Data":
        df = populate_df(type, song_name)

        display_two_tables(df)

    elif selected_tab == "Display Media Map":
        st.error("Media Map does not work for songs, please choose another search type")

    elif selected_tab == "Search Effectiveness Bar Chart":
        df = populate_df(type, song_name)

        gen_score_chart(df)

    elif selected_tab == "Song Length Scatterplot":
        df = populate_df('recording', song_name)
        num_results = st.slider("Select the number of results to display", 1, len(df), len(df))
        Generate_Scatterplot(df, num_results)

def main():
    st.title("ParaMusic")
    # horizontal menu
    selected_tab = st.radio("Select Tab", ["Filtered Data", "Raw MusicBrainz API Data", "Display Media Map", "Search Effectiveness Bar Chart", "Song Length Scatterplot"], horizontal=True)
    search_query = st.text_input("Enter a song, album, or artist name")
    search_type = st.selectbox("Search Type", ["Song", "Album", "Artist"])
    search = st.button("Search")  # The button is just for design so users feel comfortable and know the next steps after inputting text.

    if search_query:  # It is faster to detect if there is any text_input. The submit button ensures they click out of the text box
        if search_type == "Artist":
            search_artist(search_query, selected_tab)
        elif search_type == "Album":
            search_album(search_query, selected_tab)
        elif search_type == "Song":
            search_song(search_query, selected_tab)

main()
