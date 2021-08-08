from __future__ import print_function
import datetime
import os.path
import tkinter as tk
from time import sleep
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# Class to create calendar event objects
class CalendarWidget:
    def __init__(self, num=0):
        self.summary        = tk.StringVar()
        self.start          = tk.StringVar()
        self.end            = tk.StringVar()
        self.num            = num

    def update(self, calendar_update):
        self.summary.set(calendar_update[self.num]['summary'])
        if 'dateTime' in calendar_update[self.num]['start']:
            event = calendar_update[self.num]['start']['dateTime'].split('T')
            event_time = event[1].split('-')
            event_timestamp = event_time[0][:-3]
            d = datetime.datetime.strptime(event_timestamp, '%H:%M')
            self.start.set(d.strftime('%I:%M %p on ') + event[0])
        else:
            self.start.set(calendar_update[self.num]['start'].get('date'))
        self.end.set(calendar_update[self.num]['end'].get('dateTime',
                        calendar_update[self.num]['end'].get('date')))

def compareDate(d1, d2):
    for j in range(3):
        if int(d1[j]) < int(d2[j]):
            return True
        elif int(d1[j]) > int(d2[j]):
            return False
        elif j == 2:
            if len(d2) == 1:
                return False
            elif len(d1) == 1:
                return True
            else:
                d1_time = d1[1].split('-', 1)
                d2_time = d1[1].split('-', 1)
                d1_timestamp = d1_time.split(':', 1)
                d2_timestamp = d2_time.split(':', 1)

                if int(d1_timestamp[0]) < int(d2_timestamp[0]):
                    return True
                elif int(d1_timestamp[0]) > int(d2_timestamp[0]):
                    return False
                else:
                    if int(d1_timestamp[1]) < int(d2_timestamp[1]):
                        return True
                    else:
                        return False

def getCalendar():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()

    holiday_result = service.events().list(calendarId='en.usa#holiday@group.v.calendar.google.com', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    
    events = events_result.get('items', [])
    holidays = holiday_result.get('items', [])

    final_calendar = []
    list1 = 0
    list2 = 0

    for i in range(10):
        # Isolates the date and time of the event/holiday
        if 'dateTime' in events[list1]['start']:
            event_date = events[list1]['start']['dateTime'].split('T')
        else:
            event_date = events[list1]['start']['date'].split('T')
        if 'dateTime' in holidays[list2]['start']:
            holiday_date = holidays[list2]['start']['dateTime'].split('T')
        else:
            holiday_date = holidays[list2]['start']['date'].split('T')

        # Isolates the year, month, and day of the event/holiday
        event_day = event_date[0].split('-')
        holiday_day = holiday_date[0].split('-')

        if compareDate(event_day, holiday_day):
            final_calendar.append(events[list1])
            list1 += 1
        else:
            final_calendar.append(holidays[list2])
            list2 += 1
    
    if not final_calendar:
        # print('No upcoming events found.')
        no_events = []
        no_events.append('No upcoming events.')
        return no_events
    else:
        return final_calendar

# Updates calendar events every 30 mins
def calendarLoop(widget_list):
    while True:
        event_dict = getCalendar()
        for item in widget_list:
            item.update(event_dict)
        sleep(900)