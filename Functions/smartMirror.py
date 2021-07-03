'''
Author: Brandon Chang
Purpose: Main function to display information for smart mirror
'''

import tkinter as tk
import threading
from getDate import dateLoop
from getTime import timeLoop
from getWeather import WeatherWidget
from getWeather import weatherLoop
from getSpotify import spotifyLoop

timeThread = None
dateThread = None
weatherThread = None
spotifyThread = None

def greeting_frame(parent):
    global timeThread, dateThread
    var0 = tk.StringVar()
    var1 = tk.StringVar()
    var2 = tk.StringVar()

    # Label for time and greeting
    display_time = tk.Label(parent, textvariable = var0, font = 'Exo\ 2\ Light 72', bg = 'black', fg = 'white')
    display_time.pack(fill = 'x')
    display_greeting = tk.Label(parent, textvariable = var1, font = 'Exo\ 2\ Light 36', bg = 'black', fg = 'white')
    display_greeting.pack(fill = 'x')
    
    # Label for day and date
    display_date = tk.Label(parent, textvariable = var2, font = 'Exo\ 2\ Light 24', bg = 'black', fg = 'white')
    display_date.pack(fill = 'x')

    # Thread to update time continuously, checks every second
    timeThread = threading.Thread(target = timeLoop, args = (var0,var1))
    timeThread.start()

    # Thread to update date continuously, checks every 30 seconds
    dateThread = threading.Thread(target = dateLoop, args = (var2,))
    dateThread.start()

def weather_frame(parent):
    global weatherThread
    current_weather = WeatherWidget(False)

    # Frame to hold current weather information packed to the top of bottom left frame
    frame_weather_current = tk.Frame(parent)
    frame_weather_current.configure(background = 'black')
    frame_weather_current.pack(fill = 'x')

    frame_current_display = tk.Frame(frame_weather_current)
    frame_current_display.configure(background = 'black')
    frame_current_display.pack(side = 'left')
    
    # Displays city
    display_city_state = tk.Label(frame_current_display, textvariable = current_weather.city_state, font = 'Exo\ 2\ Light 18', bg = 'black', fg = 'white')
    display_city_state.pack(padx = 10)

    # Displays 'Currently" text
    display_currently = tk.Label(frame_current_display, text = 'Currently', font = 'Exo\ 2\ Light 14', bg = 'black', fg = 'white')
    display_currently.pack(padx = 10)

    # Displays current weather icon
    display_current_icon = tk.Label(frame_current_display, font = 'Weather\ Icons 40', textvariable = current_weather.icon, bg = 'black', fg = 'white')
    display_current_icon.pack(padx = 10)

    display_current_main = tk.Label(frame_current_display, textvariable = current_weather.main, 
                                    font = 'Exo\ 2\ Light 14', bg = 'black', fg = 'white')
    display_current_main.pack(padx = 10)
    
    display_current_temp = tk.Label(frame_current_display, textvariable = current_weather.temp,
                                    font = 'Exo\ 2\ Light 14', bg = 'black', fg = 'white')
    display_current_temp.pack(padx = 10)

    display_current_feels_like = tk.Label(frame_current_display, textvariable = current_weather.feels_like,
                                    font = 'Exo\ 2\ Light 12', bg = 'black', fg = 'white')
    display_current_feels_like.pack(padx = 10)

    display_current_hum = tk.Label(frame_current_display, textvariable = current_weather.hum,
                                    font = 'Exo\ 2\ Light 12', bg = 'black', fg = 'white')
    display_current_hum.pack(padx = 10)


    # Create list of weather forecast objects
    forecast_weather = []
    for day in range(5):
        forecast_weather.append(WeatherWidget(True, day))

    # Frame to hold forecast weather information packed below current weather information
    frame_weather_forecast = tk.Frame(parent)
    frame_weather_forecast.pack(pady = 30)

    for day in forecast_weather:
        frame_forecast_display = tk.Frame(frame_weather_forecast)
        frame_forecast_display.configure(background = 'black')
        frame_forecast_display.pack(side = 'left')

        display_date = tk.Label(frame_forecast_display, textvariable = day.day_date,
                                font = 'Exo\ 2\ Light 10', bg = 'black', fg = 'white')
        display_date.pack(padx = 10)

        display_icon = tk.Label(frame_forecast_display, font = 'Weather\ Icons 30', textvariable = day.day_weather_id,
                                bg = 'black', fg = 'white')
        display_icon.pack(padx = 10)

        display_main = tk.Label(frame_forecast_display, textvariable = day.day_main,
                                font = 'Exo\ 2\ Light 10', bg = 'black', fg = 'white')
        display_main.pack(padx = 10) 

        display_temp = tk.Label(frame_forecast_display, textvariable = day.day_temp,
                                font = 'Exo\ 2\ Light 10', bg = 'black', fg = 'white')
        display_temp.pack(padx = 10)

        display_hum = tk.Label(frame_forecast_display, textvariable = day.day_hum,
                                font = 'Exo\ 2\ Light 10', bg = 'black', fg = 'white')
        display_hum.pack(padx = 10)

        display_pop = tk.Label(frame_forecast_display, textvariable = day.day_pop,
                                font = 'Exo\ 2\ Light 10', bg = 'black', fg = 'white')
        display_pop.pack(padx = 10)

    # Threads for updating current & forecast weather information, checks every 30 min
    weatherThread = threading.Thread(target = weatherLoop, args = ([current_weather] + forecast_weather,))
    weatherThread.start()

def spotify_track_frame(parent):
    global spotifyThread
    var0 = tk.StringVar()
    var1 = tk.StringVar()
    var2 = tk.StringVar()

    frame_artist_display = tk.Frame(parent)
    frame_artist_display.configure(background = 'black')
    frame_artist_display.pack(fill = 'x')

    frame_track_display = tk.Frame(frame_artist_display)
    frame_track_display.configure(background = 'black')
    frame_track_display.pack()

    display_track = tk.Label(frame_track_display, textvariable = var0, font = 'Exo\ 2\ Light 16', bg = 'black', fg = 'white')
    display_track.pack()

    display_album = tk.Label(frame_track_display, textvariable = var1, font = 'Exo\ 2\ Light 16', bg = 'black', fg = 'gray')
    display_album.pack()

    display_artist = tk.Label(frame_track_display, textvariable = var2, font = 'Exo\ 2\ Light 16', bg = 'black', fg = 'gray')
    display_artist.pack()

    frame_album_display = tk.Frame(parent)
    frame_album_display.pack()
    display_album_image = tk.Label(frame_album_display)
    display_album_image.pack(side = 'bottom', fill = 'both', expand = 'yes')

    # Thread to update Spotify track, checks every second
    spotifyThread = threading.Thread(target = spotifyLoop, args = (var0, var1, var2,display_album_image))
    spotifyThread.start()

window = tk.Tk()
#window.attributes('-fullscreen', True)
window.geometry('720x900')
window.configure(background = 'black')

# Frame to hold time, greeting, and date information
frame_top = tk.Frame(window)
frame_top.configure(background = 'black')
frame_top.pack(pady = 30)

# Frame to hold weather and Spotify information below greeting frame
frame_bottom = tk.Frame(window)
frame_bottom.configure(background = 'black')
frame_bottom.pack(fill = 'x')

# Frame to hold weather information
frame_left = tk.Frame(frame_bottom)
frame_left.configure(background = 'black')
frame_left.pack(side = 'left')

# Frame to hold Spotify information
frame_right = tk.Frame(frame_bottom)
frame_right.configure(background = 'black')
frame_right.pack(side = 'right')

greeting_frame(frame_top)
weather_frame(frame_left)
spotify_track_frame(frame_right)

window.mainloop()