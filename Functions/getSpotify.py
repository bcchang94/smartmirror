'''
Author: Brandon Chang
Purpose: This function retreives 'Now Playing' information from Spotify. Displays artist/album info if music playing and gif if not
'''

import os, json, spotipy, requests
from PIL import ImageTk, Image
import tkinter as tk
from time import sleep
from spotipy.oauth2 import SpotifyOAuth


def spotifyLoop(var0, var1, var2, image_label):
    # prepares idle gif frames
    path = 'corner_store.gif'
    info = Image.open(path)
    # determines number of frames in gif
    frames = info.n_frames 
    # create list of PhotoImage objects for each frame
    im = []
    for i in range(frames):
        im.append(tk.PhotoImage(file = path, format = f"gif -index {i}"))

    count = 0
    wait_time = 5

    while True:
        spotify_dict = getSpotify()
        if spotify_dict != None and spotify_dict['is_playing'] == True:
            var0.set(spotify_dict['track_name'])
            var1.set(spotify_dict['album_name'])
            var2.set(spotify_dict['artist_name'])
            
            path = 'album_cover.jpg'
            img = ImageTk.PhotoImage(Image.open(path))
            image_label.config(image = img)
            image_label.image = img
            sleep(wait_time)
        else:
            var0.set('')
            var1.set('')
            var2.set('')

            for i in range(int(wait_time/0.2)):
                im2 = im[count]
                image_label.config(image = im2)
                count += 1
                if count == frames:
                    count = 0
                sleep(0.2)
        
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

    if current_track != None:
        # Downloads album image in working directory
        img_data = requests.get(current_track["item"]["album"]["images"][1]['url']).content
        with open('album_cover.jpg', 'wb') as handler:
                handler.write(img_data)

        #create dictionary for function return
        return_dict = {
            "album_name"    : current_track["item"]["album"]["name"],
            "artist_name"   : current_track["item"]["artists"][0]["name"],
            "track_name"    : current_track["item"]["name"],
            "is_playing"    : current_track["is_playing"]
        }
    else:
        return_dict = None

    return return_dict