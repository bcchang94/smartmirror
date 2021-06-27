'''
Author: Brandon Chang
Purpose: This function retrieves weather information from OpenWeatherMap and returns current and forecast weather reports
'''

import requests, json, os
from datetime import datetime
from time import sleep

def weatherLoop(var0, var1, var2, var3, var4):
    while True:
        getWeather(var0, var1, var2, var3, var4)
        sleep(1800)

def getWeather(var0, var1, var2, var3, var4):
    if os.path.exists('Functions/api_keys.json') == False:
        print('No API Key json file detected')

    with open('Functions/api_keys.json', 'r') as inFile:
        api_list = json.loads(inFile.read())

    if os.path.exists('Functions/weather_location.json') == False:
        print('No Weather Location json file detected')
    
    with open('Functions/weather_location.json', 'r') as inFile:
        weather_location = json.loads(inFile.read())
        
    #API Key via OpenWeatherMap
    api_key = api_list['openWeatherMap_API_Key']

    #base URL for API calls
    base_URL = 'https://api.openweathermap.org/data/2.5/onecall?'

    #provide lat & long coordinates for city of interest
    lat = weather_location["latitude"]
    lon = weather_location["longitude"]

    #provide city name
    city_name = weather_location["city"] + ', ' + weather_location["state"]

    #desired excluded information from API request
    exclude = 'minutely,hourly'

    complete_URL = base_URL + 'lat=' + lat + '&lon=' + lon + '&units=imperial' + '&exclude=' + exclude + '&appid=' + api_key

    api_response = requests.get(complete_URL)

    formatted_api_response = api_response.json()

    #create dictionary for function return
    return_dict = {}

    #entry in return_dict that has city name and state
    return_dict["city_state"] = city_name

    #retreive current weather information
    current_dict = {
        "current_temp"          : formatted_api_response["current"]["temp"],
        "current_feels_like"    : formatted_api_response["current"]["feels_like"],
        "current_humidity"      : formatted_api_response["current"]["humidity"], #documented as a percentage without %
        "current_weather_id"    : formatted_api_response["current"]["weather"][0]["id"],
        "current_weather_main"  : formatted_api_response["current"]["weather"][0]["main"]   
    }
    #determine whether to use day or night weather icon by comparing current time to sunrise/sunset time
    current_epoch = formatted_api_response["current"]["dt"]
    sunrise_epoch = formatted_api_response["current"]["sunrise"]
    sunset_epoch = formatted_api_response["current"]["sunset"]
    if current_epoch >= sunrise_epoch and current_epoch <= sunset_epoch:
        current_dict["current_icon"] = 'day'
    else:
        current_dict["current_icon"] = 'night'

    #entry in return_dict that has current weather  
    return_dict["current"] = current_dict
    
    #retreive daily weather forecast information (4 days)
    #create list to index days in forecast
    forecast_list = []
    for day in range(0,5):
        list_entry = {
            "day_date"          : datetime.fromtimestamp(formatted_api_response["daily"][day]["dt"] + formatted_api_response["timezone_offset"]).strftime("%a"), #day of the week from epoch
            "day_temp"          : formatted_api_response["daily"][day]["temp"]["day"],
            "day_humidity"      : formatted_api_response["daily"][day]["humidity"], #documented as a percentage without %
            "day_weather_id"    : formatted_api_response["daily"][day]["weather"][0]["id"],
            "day_weather_main"  : formatted_api_response["daily"][day]["weather"][0]["main"],
            "day_pop"           : formatted_api_response["daily"][day]["pop"] #documented as a decimal
        }
        forecast_list.append(list_entry)
    #entry in return_dict that has forecast weather
    return_dict["forecast"] = forecast_list

    var0.set(return_dict['city_state'])
    var1.set(return_dict['current']['current_weather_main'])
    var2.set(return_dict['current']['current_temp'])
    var3.set(return_dict['current']['current_feels_like'])
    var4.set(return_dict['current']['current_humidity'])
    
    #return return_dict

if __name__ == '__main__':
    print(getWeather())