'''
Author: Brandon Chang
'''

import os

if os.path.isdir('Functions/in_SortedHexCode') == False:
    print ('No "in" folder detected')
else:
    with open('sortHexCode.csv', 'w') as outFile:
        outFile.write('OpenWeather ID, Day Hex Code, Night Hex Code\n') #add headers to file
        for item in os.listdir('Functions/in_SortHexCode'):
            with open('Functions/in_SortHexCode' +item, 'r') as inFile:
                print('Processing' + item)
                line_