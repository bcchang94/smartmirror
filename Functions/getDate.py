'''
Author: Brandon Chang
Purpose: This function returns the date
'''

from datetime import date
from time import sleep

def dateLoop(var2):
    while True:
        getDate(var2)
        sleep(30)

def getDate(var2):
    today = date.today()
    currentDate = today.strftime('%a, %B %d')
    var2.set(currentDate)
    #return currentDate

if __name__ == '__main__':
    print(getDate())