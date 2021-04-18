'''
Author: Brandon Chang
Purpose: This function returns the time
'''

from datetime import datetime

def getTime():
    now = datetime.now()
    currentTime = now.strftime('%I:%M')
    currentHourString = now.strftime('%H')
    currentHourInt = int(currentHourString)

    if currentHourInt >= 5 and currentHourInt < 12:
        greeting = 'Good Morning'
    elif currentHourInt >= 12 and currentHourInt < 18:
        greeting = 'Good Afternoon'
    else:
        greeting = 'Good Evening'
    
    return currentTime, greeting

if __name__ == '__main__':
    print(getTime())