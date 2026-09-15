import os
import io
from pathlib import Path
import re 
import pandas as pd
from services import musicbrainz

#cleaning the artist string in case of features
def clean_string_artist(name: str)-> str:
        pattern = r'\s+(feat\.|featuring|ft\.|with|&).*$'
        cleaned = re.sub(pattern, '', name, flags=re.IGNORECASE)

        return cleaned.strip()

#parsing and cleaning the csv/txt file for the artist column
def clean_playlist(file_bytes: bytes, filename:str) -> list[str]:
    first_line = file_bytes.decode('utf-8', errors='ignore').splitlines()[0]
    delimiter = '\t' if '\t' in first_line else ','

    df = pd.read_csv(io.BytesIO(file_bytes), sep=delimiter, on_bad_lines = 'skip', engine='python')

    df.columns = [col.strip().lower() for col in df.columns]

    artist_col = next((col for col in ['artist', 'artist name'] if col in df.columns), None)
    if not artist_col:
        raise ValueError("No Valid Artist column found")

    raw_artist = df[artist_col].dropna().unique().tolist()

    cleaned_artists = {clean_string_artist(artist) for artist in raw_artist}
    return [artist for artist in cleaned_artists if artist]
    
#printing the unique artists found in the artist column
if __name__ == "__main__":
        example_file_path = Path(__file__).parent / "example.txt"

        if not example_file_path.exists():
            print("Example file not found! Add a playlist .txt file into this folder")
        else:
            with open(example_file_path, "rb") as f:
                file_contents = f.read()

            try: 
                artists = clean_playlist(file_contents,example_file_path.name)
                print(f"Parsing Success\n{len(artists)} unique artists found in your playlist: ")
                for i, artist in enumerate(artists, 1):
                     print(f" {i}. {artist}")
            except Exception as e:
                 print(f"Error parsing file: {e}")

        artists_mbids = {}
        for artist in artist:
             mbid = musicbrainz.py(artist)

