import pandas as pd
import io

def parse_playlist(file_bytes: bytes) -> list[dict]:
    df = pd.read_csv(io.BytesIO(file_bytes))
    df.colums = df.colums.str.strip().str.lower()

    df = df.dropna(subset=['name', 'artist', 'album', 'genre'])
    return df[['name', 'artist', 'album', 'genre']].to_dict(orient='records')