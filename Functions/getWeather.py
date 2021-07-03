'''
Author: Brandon Chang
Purpose: These functions retrieve weather information from OpenWeatherMap and returns current and forecast weather reports
'''
import tkinter as tk
import requests, json, os
from datetime import datetime
from time import sleep

if os.path.exists('hexCode.json') == False:
    print('No json hex code file detected')
        
with open('hexCode.json', 'r') as inFile:
    hexCode_dict = json.loads(inFile.read())

class WeatherWidget:
    def __init__(self, isForecast, num=0):
         # object for forecast weather
        if isForecast:
            self.day_date           = tk.StringVar()
            self.day_weather_id     = tk.StringVar()
            self.day_main           = tk.StringVar()
            self.day_temp           = tk.StringVar()
            self.day_hum            = tk.StringVar()
            self.day_pop            = tk.StringVar()
            self.day_num            = num
        # object for current weather
        else:
            self.city_state         = tk.StringVar()
            self.icon               = tk.StringVar()
            self.main               = tk.StringVar()
            self.temp               = tk.StringVar()
            self.feels_like         = tk.StringVar()
            self.hum                = tk.StringVar()
        
        self.isForecast = isForecast
    
    def update(self, weather_update):
        if self.isForecast:
            self.day_date.set(weather_update['forecast'][self.day_num]['day_date'])
            self.day_weather_id.set(self.weatherIcon(weather_update))
            self.day_main.set(weather_update['forecast'][self.day_num]['day_weather_main'])
            self.day_temp.set(weather_update['forecast'][self.day_num]['day_temp'])
            self.day_hum.set('Hum: ' + str(weather_update['forecast'][self.day_num]['day_humidity']) + '%')
            self.day_pop.set('Pop: ' + str(weather_update['forecast'][self.day_num]['day_pop'] * 100) + '%')
        else:
            self.city_state.set(weather_update['city_state'])
            self.icon.set(self.weatherIcon(weather_update))
            self.main.set(weather_update['current']['current_weather_main'])
            self.temp.set(weather_update['current']['current_temp'])
            self.feels_like.set('Feels like: ' + str(weather_update['current']['current_feels_like']))
            self.hum.set('Hum: ' + str(weather_update['current']['current_humidity']) + '%')

    def weatherIcon(self, weather_dict):
        if self.isForecast:
            # Updating forecast weather icons
            forecast_weather_id = str(weather_dict['forecast'][self.day_num]['day_weather_id'])
            return chr(int('0x' + hexCode_dict[forecast_weather_id][0], 16))
        else:
            # Updating current weather icon
            current_weather_id = str(weather_dict['current']['current_weather_id'])
            current_icon = weather_dict['current']['current_icon']

            if current_icon == 'day':
                return chr(int('0x' + hexCode_dict[current_weather_id][0], 16))
            elif current_icon == 'night':
                return chr(int('0x' + hexCode_dict[current_weather_id][1], 16))

def getWeather():
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
    for day in range(5):
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

    #updates return_dict to include hex character weather icons instead of ID
    #return_dict = self.weatherIcon(return_dict)
    
    return return_dict           

def weatherLoop(widget_list):
    while True:
        weather_dict = getWeather()
        for item in widget_list:
            item.update(weather_dict)
        sleep(1800)

# if __name__ == '__main__':
#     print(getWeather())