'''
Author: Brandon Chang
'''

import os

if os.path.isdir('Functions/in_SortedHexCode') == False:
    print ('No "in" folder detected')
else:
    with open('sortHexCode.csv', 'w') as outFile:
        outFile.write('OpenWeather ID, Day Hex Code, Night Hex Code\n') #add headers to file
        for item in os.listdir('Functions/in_SortedHexCode'):
            with open('Functions/in_SortedHexCode/' +item, 'r') as inFile:
                print('Processing ' + item)
                #line_A = inFile.readline()
                #line_A = inFile.readline()
                #openWeatherID_A = line_A[0][-3:]
                #hexCodeChar_A = line_A[1]
                #line_B = inFile.readline()
                #openWeatherID_B = line_B[0][-3:]
                #hexCodeChar_B = line_B[1]
                row_count = len(list(inFile)) #determine number of rows in csv file
                List = [None] * (row_count-1) #-1 to exclude header
                line = inFile.readline()
                print(line)
                for row in range(row_count-1):
                    List[row] = line
                    
                    line = inFile.readline()
                    #print(List[0])
