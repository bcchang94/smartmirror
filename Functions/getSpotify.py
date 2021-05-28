'''
Author: Brandon Chang
Purpose: This function retreives 'Now Playing' information from Spotify
'''

import os, json, spotipy, requests
from spotipy.oauth2 import SpotifyOAuth

def getSpotify():
    if os.path.exists('Functions/api_keys.json') == False:
        print('No API Key json file detected')

    with open ('Functions/api_keys.json', 'r') as inFile:
        api_list = json.loads(inFile.read())

    client_id = api_list['spotify_client_id']

    sp = spotipy.oauth2.SpotifyPKCE(client_id=client_id,
                                    redirect_uri="http://localhost:8080",
                                    scope='user-library-read,user-read-currently-playing', 
                                    open_browser=False)
    
    #determines if cache has been created for access token
    if sp.get_cached_token():
        access_token = sp.get_access_token()
    
    #creates new access token if no cache present 
    else:
        access_token = sp.refresh_access_token(api_list['spotify_refresh_token'])
    
    current_track = spotipy.client.Spotify(auth=access_token).currently_playing()
    #print(current_track)

    img_data = requests.get(current_track["item"]["album"]["images"][1]['url']).content
    with open('album_cover.jpg', 'wb') as handler:
            handler.write(img_data)

    #create dictionary for function return
    return_dict = {
        #"album_cover"   : current_track["item"]["album"]["images"][1],
        "album_name"    : current_track["item"]["album"]["name"],
        "artist_name"   : current_track["item"]["artists"][0]["name"],
        "track_name"    : current_track["item"]["name"]
    }

    return return_dict

if __name__ == '__main__':
    print(getSpotify())