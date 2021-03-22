'''
Author: Brandon Chang
'''

import os

if os.path.isdir('Functions/in_API Mapping') == False:
    print('No "in" folder detected')
else:
    with open('processAPIMapping.csv', 'w') as outFile:
        outFile.write('OpenWeather ID, Hex Code Character\n') #add headers to file
        for item in os.listdir('Functions/in_API Mapping'):
            with open('Functions/in_API Mapping/'+item, 'r') as inFile:
                print('Processing '+ item)
                line = inFile.readline() #reads in first line in file
                while line!= '': #run while there's still content
                    noSpace = ' '.join(line.split()) #remove leading, trailing, and duplicate whitespace
                    cols = noSpace.split() #creates an array for each column, split with white space
                    OWID = cols[0]
                    hexChar = cols[1]
                    outFile.write('{},{}\n'.format(OWID,hexChar))
                    line = inFile.readline()
                    if '\n' in line:
                        line = inFile.readline()
print('Done')
os.system('PAUSE')