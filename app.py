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
        country_filter = st.text_input("Filter by Country", "")
        submit_button = st.button('Apply Filter')

        if submit_button and country_filter:
            search_url = f"{base_url}area/"
            params = {'query': country_filter, 'fmt': 'json'}
            country_results = make_request(search_url, params)

            if country_results:
                country_df = [{"Country": country.get('name', 'N/A'),
                               "Latitude": country.get('coordinates', {}).get('latitude', 'N/A'),
                               "Longitude": country.get('coordinates', {}).get('longitude', 'N/A')} for country in
                              country_results['areas']]
                country_df = [entry for entry in country_df if
                              all(entry.values())]  # Remove entries with missing latitude or longitude
                if country_df:
                    fig = px.scatter_geo(country_df, locations="Country", locationmode="country names",
                                         color="Latitude", size="Longitude",
                                         hover_name="Country", size_max=40, template="plotly",
                                         projection="natural earth")
                    st.plotly_chart(fig)
                else:
                    st.warning("No valid coordinates found for the entered country.")
            else:
                st.warning("Country information not found.")

    elif selected_tab == "Artist Information":
        artist_id = st.text_input("Enter Artist ID", "")
        submit_button = st.button('Get Information')

        if submit_button and artist_id:
            search_url = f"{base_url}artist/{artist_id}"
            params = {'fmt': 'json'}
            results = make_request(search_url, params)
            if results:
                    st.write(f"Name: {results.get('name', 'N/A')}")
                    st.write(f"Country: {results.get('country', 'N/A')}")
                # Add more information as needed
            else:
                st.warning("Artist information not found.")

def search_album(album_name, selected_tab):
    if selected_tab == "Raw MusicBrainz API Data":
        search_url = f"{base_url}release/"
        params = {'query': album_name, 'fmt': 'json'}
        results = make_request(search_url, params)
        df = produce_dataframe(results, 'releases')
        st.table(df)

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
        country_filter = st.text_input("Filter by Country", "")
        submit_button = st.button('Apply Filter')

        if submit_button and country_filter:
            search_url = f"{base_url}area/"
            params = {'query': country_filter, 'fmt': 'json'}
            country_results = make_request(search_url, params)

            print("Country Results:", country_results)  # Print the results for debugging

            if country_results and 'areas' in country_results:
                country_df = [{"Country": country.get('name', 'N/A'),
                               "Latitude": country.get('coordinates', {}).get('latitude', 'N/A'),
                               "Longitude": country.get('coordinates', {}).get('longitude', 'N/A')} for country in
                              country_results['areas']]
                country_df = [entry for entry in country_df if
                              all(entry.values())]  # Remove entries with missing latitude or longitude
                if country_df:
                    fig = px.scatter_geo(country_df, locations="Country", locationmode="country names",
                                         color="Latitude", size="Longitude",
                                         hover_name="Country", size_max=40, template="plotly",
                                         projection="natural earth")
                    st.plotly_chart(fig)
                else:
                    st.warning("No valid coordinates found for the entered country.")
            else:
                st.warning("Country information not found.")

    elif selected_tab == "Release Events":
        # Add logic for filtered data
        pass

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
    elif selected_tab == "Length of songs":
        # Add logic for filtered data
        pass

def main():
    st.title("ParaMusic")
    search_query = st.text_input("Enter a song, album, or artist name")
    search_type = st.selectbox("Search Type", ["Song", "Album", "Artist"])

    st.sidebar.subheader("Search Options")
    selected_tab = st.sidebar.radio("Select Tab", ["Raw MusicBrainz API Data", "Filtered Data", "Artist Information", "Search Effectiveness Bar Chart"])

    if st.button("Search"):
        if search_type == "Artist":
            search_artist(search_query, selected_tab)
        elif search_type == "Album":
            search_album(search_query, selected_tab)
        elif search_type == "Song":
            search_song(search_query, selected_tab)


main()
