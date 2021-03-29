'''
Author: Brandon Chang
'''

import os

if os.path.isdir('Functions/in_ProcessHexCode') == False:
    print ('No "in" folder detected')
else:
    with open('sortHexCode.csv', 'w') as outFile:
        outFile.write('OpenWeather ID, Day Hex Code, Night Hex Code\n') #add headers to file
        for item in os.listdir('Functions/in_ProcessHexCode'):
            with open('Functions/in_ProcessHexCode/' +item, 'r') as inFile:
                print('Processing ' + item)
                contents = inFile.read().split('\n') #read in whole file and split at \n
                contents_formatted = contents.split(',') #split element in array into two strings using comma