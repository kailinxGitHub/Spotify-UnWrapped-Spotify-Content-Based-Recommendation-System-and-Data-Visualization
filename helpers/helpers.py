# cleans the url to get the Spotify ID
def clean_spotify_url_id(url):
    if url:
        return url.split('/')[-1]
    return None