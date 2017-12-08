#!/usr/bin/python3

"""
Purpose - 
To demonstrate how you can interact with Google Calendar APIs
Pre-requisites - 
1. Project in Google Developers console (API is enabled)
2. client_secret.json is available in working directory
3. google-api-python-client is installed, If not, use the similar commmand
pip3 install --upgrade google-api-python-client

Official Documentation -
https://developers.google.com/google-apps/calendar/quickstart/python
"""

from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json

#SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                'calendar-python-quickstart.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials
                            
def main():
    """Shows basic usage of the Google Calendar API.

        Creates a Google Calendar API service object and outputs a list of the next
        10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the next event')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=1, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
        #Logic to check if meeting is in progress
        print(event)
        print(event['htmlLink'].split("=")[-1])
        #print(event['start'].get('date'))
        #event_id = event['htmlLink'].split("=")[-1]
        event_id = event['id']
        meeting_start_time = datetime.datetime.strptime("-".join(start.split("-")[:-1]), '%Y-%m-%dT%H:%M:%S')
        if datetime.datetime.now() >= meeting_start_time: 
            print("Time to auto remove this event as it seems room is vacant")
            #service.events().delete(calendarId='primary', eventId='eventId').execute()
            print(event_id)
            service.events().delete(calendarId='primary', eventId=event_id).execute()

if __name__ == '__main__':
    main()
