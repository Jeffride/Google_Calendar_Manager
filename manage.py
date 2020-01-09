from __future__ import print_function
from datetime import datetime, timedelta
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly',
          'https://www.googleapis.com/auth/calendar.events',
          'https://www.googleapis.com/auth/calendar'
          ]

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

    inpt = raw_input("Do you want to input a new event: ")

    if inpt != 'no':
        create_event(service)
    else:
        pass


def create_event(service):



    days_dict = {
        'mon':0,
        'tues':1,
        'wed':2,
        'thur':3,
        'fri':4,
        'sat':5,
        'sun':6,
    }



    #start_time = '22:00'
    #end_time = '23:00'



    days = raw_input("what days are you working this week[mon,tues,wed,thur,fri,sat,sun](seperate by comma): ")
    daylist = days.split(",")

    for day in daylist:
        today = datetime.date.today()
        day_num = int(today.weekday())
        num = int(days_dict[day])
        event = str("event"+str(num))

        event = {
            'summary': 'Work',
            'location': 'Home Store + More',
            'description': '',
            'start': {
                'dateTime': '',
                'timeZone': 'GB-Eire',
            },
            'end': {
                'dateTime': '',
                'timeZone': 'GB-Eire',
            },
            'recurrence': [
                'RRULE:FREQ=DAILY;COUNT=1'
            ],
            'attendees': [
            ],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'popup', 'minutes': 30},
                ],
            },
        }


        add = num - day_num
        wday = today + timedelta(days=add)


        start_time = raw_input("please input start time on "+day+"(00:00 format): ")
        end_time = raw_input("please input end time on "+day+"(00:00 format): ")

        start = str(wday)+"T"+str(start_time)+":00.0z"
        event['start']['dateTime']=start

        end = str(wday)+"T"+str(end_time)+":00.0z"
        event['end']['dateTime']=end


        event = service.events().insert(calendarId='primary', body=event).execute()
        print('Event created:%s' %(event.get('htmlLink')))



if __name__ == '__main__':
    main()
