'''
Author: Brandon Chang
Purpose: This function returns the date
'''

from datetime import date

def getDate():
    today = date.today()
    currentDate = today.strftime('%a, %B %d')
    return currentDate

if __name__ == '__main__':
    print(getDate())

