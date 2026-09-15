import musicbrainzngs

musicbrainzngs.set_useragent(
    "PlayMe",
    "0.1",
    "https://github.com/kayco00/PlayMe"
)

def musicLookup(artist_name:str):

    try:
        result = musicbrainzngs.search_artists(artist=artist_name, limit=1)
        artist_list = result.get("artist-list",[])

        if not artist_list:
            print("Artist Not Found")
            return

        first_match = artist_list[0]
        artist_id = first_match["id"]
        cannon_name = first_match["name"]

        print(f"Artist Found")
        print(f"MBID: {artist_id}")

    except musicbrainzngs.WebServiceError as e:
        print(f"Web Service Error: {e}")
    except Exception as e:
        print(f"Error Occurred: {e}")
