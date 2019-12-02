from __future__ import print_function
import datetime
import pickle
import os.path
import random
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def checkForPracticeInserts(service, e1EndTime, e2StartTime):
    wait = e2StartTime - e1EndTime
    wait = abs(divmod(wait.total_seconds(), 3600)[0])
    #if there is more than a 2 hour gap between events,  pick a random event from list
    if wait > 2:
        cur = 0.25
        stop = wait - 1.25
        while cur <= stop:
            curTime = e1EndTime + datetime.timedelta(hours = cur)
            print(curTime)
            curTimePlusHR = curTime + datetime.timedelta(hours = 1)
            #pick 
            e = random.choice(["""events"""])
            event = {
                'summary': e,
                'start': {
                    'dateTime': curTime.isoformat(),
                    'timeZone': 'America/Los_Angeles',
                },
                'end': {
                    'dateTime': curTimePlusHR.isoformat(),
                    'timeZone': 'America/Los_Angeles',
                },
                'colorId': {
                    'colorId': "4"
                },
                'reminders': {
                    'useDefault': False
                },
            }
            event = service.events().insert(calendarId='primary', body=event).execute()
            print('Event created: %s'% (event.get('htmlLink')))
            cur += 1
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
    # Change to PST
    utcToPst = datetime.timedelta(hours=-8, minutes = 0, seconds = 0) 
    pstTZ= datetime.timezone(utcToPst, name="PST")
    now = datetime.datetime.now()
    today =datetime.datetime(now.year,now.month,now.day)
    today = today.replace(tzinfo = pstTZ)

    for day in range(1,8):
        print("day num " + str(day))
        nextTime = datetime.datetime.strptime(str(today).split(" ")[0],'%Y-%m-%d')
        nextTime += datetime.timedelta(days = 1)
        nextTime = datetime.datetime(nextTime.year, nextTime.month, nextTime.day)
        nextTime = nextTime.replace(tzinfo = pstTZ)

        events_result = service.events().list(calendarId='primary', timeMin=today.isoformat(),
                                         timeMax = nextTime.isoformat(), singleEvents=True,
                                        orderBy='startTime').execute()
        events = events_result.get('items', [])
        eventsKeep = []
        for event in events:
            if "T" in event['start'].get('dateTime', event['start'].get('date')):
                eventsKeep.append(event)

        for event in range(len(eventsKeep)):
            if event  == 0:
                #pick own hour each day for waking up
                wake = datetime.datetime(today.year, today.month, today.day, hour = #INPUT)
                wake = wake.replace(tzinfo = pstTZ)
                checkForPracticeInserts(service, wake, datetime.datetime.fromisoformat(eventsKeep[event]['start'].get('dateTime', eventsKeep[event]['start'].get('date'))))
                
            if event == len(eventsKeep)-1:
                #Pick own hour to stop scheduling
                goBed = datetime.datetime(today.year, today.month, today.day, hour = #INPUT).replace(tzinfo = pstTZ)
                checkForPracticeInserts(service, datetime.datetime.fromisoformat(eventsKeep[event]['end'].get('dateTime', eventsKeep[event]['end'].get('date'))),goBed)
                
            if event != 0:
                e1end = datetime.datetime.fromisoformat(eventsKeep[event-1]['end'].get('dateTime', eventsKeep[event-1]['end'].get('date')))
                e2start = datetime.datetime.fromisoformat(eventsKeep[event]['start'].get('dateTime', eventsKeep[event]['start'].get('date')))
                checkForPracticeInserts(service, e1end, e2start)

        for event in eventsKeep:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
        #incriment what "today" is 
        today = nextTime




    

if __name__ == '__main__':
    main()