'''
Author: Brandon Chang
Purpose: Main function to display information for smart mirror
'''

import tkinter as tk
from getDate import getDate
from getTime import getTime
from getWeather import getWeather
from getSpotify import getSpotify

def greeting_frame():
    time = getTime()
    display_time = tk.Label(frame_top, text = time[0])
    display_time.pack()
    display_greeting = tk.Label(frame_top, text = time[1])
    display_greeting.pack()
    
    date = getDate()
    display_date = tk.Label(frame_top, text = '\n' + date)
    display_date.pack()

def current_weather_frame():
    # Frame to hold current weather information packed to the top of bottom left frame
    frame_weather_current = tk.Frame(frame_left)
    frame_weather_current.pack(fill = 'x')

    frame_current_display = tk.Frame(frame_weather_current)
    frame_current_display.pack(side = 'left')

    display_city_state = tk.Label(frame_current_display, text = weather_dict['city_state'])
    display_city_state.pack(padx = 10)

    display_currently = tk.Label(frame_current_display, text = 'Currently')
    display_currently.pack(padx = 10)

    display_current_icon = tk.Label(frame_current_display, font = 'Weather\ Icons 30', text = chr(0xf010))
    display_current_icon.pack(padx = 10)

    display_current_main = tk.Label(frame_current_display, text = weather_dict['current']['current_weather_main'])
    display_current_main.pack(padx = 10)

    display_current_temp = tk.Label(frame_current_display, text = weather_dict['current']['current_temp'])
    display_current_temp.pack(padx = 10)

    display_current_feels_like = tk.Label(frame_current_display, text = 'Feels like: ' + str(weather_dict['current']['current_feels_like']))
    display_current_feels_like.pack(padx = 10)

    display_current_hum = tk.Label(frame_current_display, text = 'Hum: ' + str(weather_dict['current']['current_humidity']) + '%')
    display_current_hum.pack(padx = 10)

def forecast_weather_frame():
    # Frame to hold forecast weather information packed below current weather information
    frame_weather_forecast = tk.Frame(frame_left)
    frame_weather_forecast.pack(pady = 30)

    for i in range(5):
        frame_forecast_display = tk.Frame(frame_weather_forecast)
        frame_forecast_display.pack(side = 'left')

        display_date = tk.Label(frame_forecast_display, text = weather_dict['forecast'][i]['day_date'])
        display_date.pack(padx = 10)

        display_icon = tk.Label(frame_forecast_display, font = 'Weather\ Icons 30', text = chr(0xf005))
        display_icon.pack(padx = 10)

        display_main = tk.Label(frame_forecast_display, text = weather_dict['forecast'][i]['day_weather_main'])
        display_main.pack(padx = 10)

        display_temp = tk.Label(frame_forecast_display, text = weather_dict['forecast'][i]['day_temp'])
        display_temp.pack(padx = 10) 

        display_hum = tk.Label(frame_forecast_display, text = 'Hum: ' + str(weather_dict['forecast'][i]['day_humidity']) + '%')
        display_hum.pack(padx = 10)

        display_pop = tk.Label(frame_forecast_display, text = 'Pop: ' + str(weather_dict['forecast'][i]['day_pop']) + '%')
        display_pop.pack(padx = 10)

window = tk.Tk()
#window.attributes('-fullscreen', True)
window.geometry('720x900')

# Frame to hold time, greeting, and date information
frame_top = tk.Frame(window)
frame_top.pack(pady = 30)

# Frame to hold weather and Spotify information below greeting frame
frame_bottom = tk.Frame(window)
frame_bottom.pack(fill = 'x')

# Frame to hold weather information
frame_left = tk.Frame(frame_bottom)
frame_left.pack(side = 'left')

# Frame to hold Spotify information
frame_right = tk.Frame(frame_bottom)
frame_right.pack(side = 'right')

# Retrieve weather API information
weather_dict = getWeather()

greeting_frame()
current_weather_frame()
forecast_weather_frame()

window.mainloop()