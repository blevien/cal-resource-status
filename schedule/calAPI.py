from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .models import Calendar, Event, Display, Location
from datetime import datetime, timedelta

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

class EventsAPI:
    def __init__(self):
        self.creds = None

        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())
    
    def get_events(self, calendar_name):
        try:
            service = build('calendar', 'v3', credentials=self.creds)

            # Set the Start/End base on current
            start = datetime.now()
            start = start.replace(hour=0, minute=0, second=0, microsecond=1)
            end = start + timedelta(days=7)
            end = end.replace(hour=23, minute=59, second=59, microsecond=999999)

            # Set Up Calendar ID
            print(calendar_name)
            calendarID = Calendar.objects.get(summary=calendar_name).url
            #calendarID = 'c_92b38e8ecacdf175ed86b2f41a37443b60af1b288cb0e96103fedff6df5b639b@group.calendar.google.com'
            
            # Call the Calendar API
            events_result = service.events().list(calendarId=calendarID, 
                                                timeMin=start.isoformat() + '-10:00',
                                                timeMax=end.isoformat() + '-10:00',
                                                timeZone='Pacific/Honolulu',
                                                singleEvents=True,
                                                orderBy='startTime').execute()
             
            # Return a list of Items in the API Response
            for event in events_result.get("items", []):
                try:
                    existing_event = Event.objects.get(custom_id=event['id'])
                    existing_event.summary = event['summary']

                    format = '%Y-%m-%dT%H:%M:%S%z'
                    existing_event.start = datetime.strptime(event['start']['dateTime'], format)
                    existing_event.end = datetime.strptime(event['end']['dateTime'], format)

                    try:
                        for location in event['location'].split(','):

                            location = location.strip()

                            try:
                                existing_location = Location.objects.get(name=location)
                                existing_event.locations.add(existing_location) 

                            except Location.DoesNotExist:
                                new_location = Location.objects.create(name=location)
                                new_location.save()
                                existing_event.locations.add(new_location)
                    except KeyError:
                        pass  
                                
                    event_calendar = Calendar.objects.get(summary=events_result.get("summary").strip())
                    existing_event.calendar = event_calendar
                    existing_event.save()

                except Event.DoesNotExist:

                    summary = event['summary']

                    format = '%Y-%m-%dT%H:%M:%S%z'
                    start = datetime.strptime(event['start']['dateTime'], format)
                    end = datetime.strptime(event['end']['dateTime'], format)
                                
                    new_event = Event.objects.create(custom_id=event['id'], 
                                                start=start, 
                                                end=end, 
                                                summary=summary,
                                                calendar=Calendar.objects.get(summary=calendar_name))
                    new_event.save()
                    
                    try:
                        for location in event['location'].split(','):

                            location = location.strip()

                            try:
                                existing_location = Location.objects.get(name=location)
                                new_event.locations.add(existing_location) 

                            except Location.DoesNotExist:
                                new_location = Location.objects.create(name=location)
                                new_location.save() 
                                new_event.locations.add(new_location)
                    except KeyError:
                        pass

            return events_result


        except HttpError as error:
            print('An error occurred: %s' % error)
            return False


def main():
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

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Set the Start/End base on current
        start = datetime.datetime.now() + datetime.timedelta(days=28)
        end = start + datetime.timedelta(days=7)

        # Set Up Calendar ID
        calendarID = 'c_ecb3b5fef7470ed518f2fd88615ad1c8c58ef35a2c7af2ef406ea3921cde0e64@group.calendar.google.com'
        print('Getting this week\'s events...')
        
        # Call the Calendar API
        events_result = service.events().list(calendarId=calendarID, 
                                              timeMin=start.isoformat() + 'Z',
                                              timeMax=end.isoformat() + 'Z',
                                              singleEvents=True,
                                              orderBy='startTime').execute()
        
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        # Prints the start and name of the next 10 events
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])

    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()