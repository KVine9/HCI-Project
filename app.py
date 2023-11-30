import requests

def search_artist(artist_name):
    base_url = "https://musicbrainz.org/ws/2/"
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
                print(f"Name: {artist['name']}, ID: {artist['id']}")
        else:
            print("No artists found.")
    else:
        print(f"Error: {response.status_code}")

# Example usage
search_artist("Metallica")
