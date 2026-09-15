
import time
import re
import ssl
import certifi
import musicbrainzngs

def setup_musicbrainz():

    ssl._create_default_https_context = lambda:ssl.create_default_context(cafile=certifi.where())

    musicbrainzngs.set_useragent(
        app="PlayMe",
        version="0.7.1",
        contact="https://github.com/kayco00/PlayMe"
)

def clean_string_artist(name: str) -> str:
    pattern = r'\s+(feat\.|featuring|ft\.|with|&).*$'
    cleaned = re.sub(pattern, '', name, flags=re.IGNORECASE)
    return cleaned.strip()

def musicLookup(artist_name:str) -> str | None:

    try:

        time.sleep(1.0)
        cleaned_name = clean_string_artist(artist_name)
        query_str = f'artist:"{cleaned_name}"'
        result = musicbrainzngs.search_artists(query=query_str, limit=1)
        artist_list = result.get("artist-list",[])

        if not artist_list:
            result = musicbrainzngs.search_artists(
                artist = cleaned_name, limit=1
            )
            artist_list = result.get("artist-list",[])

        if artist_list:
            match = artist_list[0]
            mbid = match.get("id")
            name = match.get("name")
            print(f" Found: '{artist_name}' - '{name}' (MBID: {mbid})")
            return mbid

        else:
            print("No Match Found in API")
            return None

    except Exception as e:
        print(f"MusicBrainz Error for {artist_name}'.")
        return None

