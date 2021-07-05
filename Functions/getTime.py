'''
Author: Brandon Chang
Purpose: This function returns the time
'''

from datetime import datetime
from time import sleep

def timeLoop(var0,var1):
    while True:
        getTime(var0,var1)
        sleep(1)

def getTime(var0, var1):
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

    var0.set(currentTime)
    var1.set(greeting)