'''
Author: Brandon Chang
'''

import requests, json, os

if os.path.exists('Functions/api_keys.json') == False:
    print('No API Key json file detected')

with open('Functions/api_keys.json', 'r') as inFile:
    api_list = json.loads(inFile.read())
    
#API Key via OpenWeatherMap
api_key = api_list['openWeatherMap_API_Key']

#base URL for API calls
base_URL = 'https://api.openweathermap.org/data/2.5/onecall?'

#provide lat & long coordinates for city of interest
lat = '33.4936'
lon = '117.1484'

#provide city name
city_name = 'Temecula, CA'

#desired excluded information from API request
exclude = 'minutely'

complete_URL = base_URL + 'lat=' + lat + '&lon=' + lon + '&units=imperial' + '&exclude=' + exclude + '&appid=' + api_key

api_response = requests.get(complete_URL)

format_api_response = api_response.json()
print(format_api_response)