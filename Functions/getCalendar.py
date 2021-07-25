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
        self.start.set(calendar_update[self.num]['start'].get('dateTime', 
                        calendar_update[self.num]['start'].get('date')))
        self.end.set(calendar_update[self.num]['end'].get('dateTime',
                        calendar_update[self.num]['end'].get('date')))

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
    #print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        # print('No upcoming events found.')
        no_events = []
        no_events.append('No upcoming events.')
        return no_events
    else:
        return events
    # for event in events:
    #     start = event['start'].get('dateTime', event['start'].get('date'))
    #     print(start, event['summary'])

# Updates calendar events every 30 mins
def calendarLoop(widget_list):
    while True:
        event_dict = getCalendar()
        for item in widget_list:
            item.update(event_dict)
        sleep(5)

# if __name__ == '__main__':
#     getCalendar()