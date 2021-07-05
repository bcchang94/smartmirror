# Smart Mirror
## Overview
Collection of code to implement a smart mirror. This smart mirror in particular displays:
- Date
- Time/Greeting
- Current and forecasted weather
- Spotify "Now Playing" track with artist, album, and album cover information
    - A gif will display if no music is playing (i.e. Idle State)

Project is written completely in Python.

## Table of Contents
* [getTime](#getTime)
* [getDate](#getDate)
* [processAPIMapping](#processAPIMapping)
* [processHexCode](#processHexCode)
* [getWeather](#getWeather)
* [getSpotify](#getSpotify)
* [smartMirror](#smartMirror)

## getTime
Required libraries:
- datetime
- time

Retrieves the current time and its corresponding greeting. Time is checked every 1 second.

## getDate
Required libraries:
- datetime
- time

Retreives the current date. Text is formatted to display abbreviated day of the week, month, and date. Date is checked every 30 seconds.

## processAPIMapping
Required libraries:
- os

Weather API for this project is [OpenWeatherMap](https://openweathermap.org/). The "One Call API" option was utilized. However, the native weather icons were not implemented.

Unique weather icons were downloaded from [Erik Flowers' GitHub](https://erikflowers.github.io/weather-icons/). He has taken the liberty to map different weather API weather forecasts with his icons. Setup procedure is documented in the link.

This function converts the "icon to API mapping" text file to a csv file.

## processHexCode
Required libraries:
- os
- json

Utilizing the csv file generated from the previous section, a json file is created that links the weather ID provided from the API call to a hex character. The icons also change depending on the time (i.e. day vs night).

## getWeather
Required libraries:
- tkinter
- requests
- json
- os
- datetime
- time

A class of weather widgets is created for the current weather as well as for each day in the forecast. An API request will return all the desired weather infomration in a formatted dictionary that can be accessed for updating.

The json file created from the previous section is used to link the corresponding icon hex character to the weather forecast. A separate json file called "weather_location.json" exists for the user to update their city, latitude, and longitude location.

Weather forecasts requests are performed every 30 minutes.

## getSpotify
Required libraries:
- os
- json
- spotipy
- requests
- PIL
- tkinter
- time
- spotipy.oauth2

[Spotipy](https://spotipy.readthedocs.io/en/2.18.0/#) is a library designed to simplify interfacing with Spotify's API. There is an authentification process that must be performed for login.

A Spotify request is performed to retreive the user's currently playing track. The track's name, album name, artist name, and album cover are returned in a formatted dictionary. These requests are performed every 5 seconds. If no track is playing, a gif is displayed instead.

## smartMirror
Required libraries:
- tkinter
- threading

Import functions:
- getDate
- getTime
- getWeather
- getSpotify

This is the main function that will display all the information from the imported functions on a GUI via tkinter. Threads are created for each function so that the updates can be performed at different frequencies. 