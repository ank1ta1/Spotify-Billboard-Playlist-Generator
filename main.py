from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
#user id = $$$

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id='###',
        client_secret='###',
        show_dialog=True,
        cache_path="###"
    )
)

# print("USER", sp.current_user())
# user_id = sp.current_user()["id"]


date = input("Which year do you want to travel to? Type the date in this format: YYYY-MM-DD: ")

response = requests.get("https://www.billboard.com/charts/hot-100/" + date)
bb_webpage = response.text

soup = BeautifulSoup(bb_webpage, "html.parser")

songs = soup.find_all("h3", class_='u-line-height-normal@mobile-max')

# print(songs)
song_names = []
for song in songs:
    song_names.append(song.getText())
print(song_names)

user_id = sp.current_user()["id"]
#date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
# print(playlist)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)




