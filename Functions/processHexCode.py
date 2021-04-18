'''
Author: Brandon Chang
Purpose: Formats csv OpenWeather mapped icons to json file, linking ID with daytime icon as first entry and nighttime icon as second entry
'''

import os
import json

if os.path.isdir('Functions/in_ProcessHexCode') == False:
    print ('No "in" folder detected')
else:
    with open('sortHexCode.csv', 'w') as outFile:
        outFile.write('OpenWeather ID, Day Hex Code, Night Hex Code\n') #add headers to file
        for item in os.listdir('Functions/in_ProcessHexCode'):
            with open('Functions/in_ProcessHexCode/' +item, 'r') as inFile:
                print('Processing ' + item)
                contents = inFile.readlines() #read in whole file, stores each line as a list item
                contents_formatted = [] 
                for contents_item in contents:
                    contents_formatted.append(contents_item.split(',')) #append to list, creates list of lists with two strings
                contents_final = [[x[0][-3:], x[1].strip()] for x in contents_formatted] #creates new list that's same size as contents_formatted with additional formatting
                del contents_final[0]
                icon_dict = {} 
                for x in contents_final: 
                    if x[0] in icon_dict: #appends to dictionary entry if duplicate key is found
                        icon_dict[x[0]].append(x[1]) #note append only works with lists, not strings
                    else: #creates new key if it is the first instance of the key, elements must be in a list format
                        icon_dict[x[0]] = [x[1]]
                with open('hexCode.json', 'w') as outFile: #outputs icon_dict as a json file
                    json.dump(icon_dict, outFile)