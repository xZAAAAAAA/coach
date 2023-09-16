from __future__ import print_function

import datetime
import os.path

import pytz

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar" ]


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
        print("Getting the upcoming 10 events")
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        # xd = service.events().watch(calendarId='primary', body={
        #     'id': 'choach_uniq_id3421',
        #     'type': 'web_hook',
        #     'address': 'https://bf8f-85-214-57-62.ngrok-free.app/calupdates',
        # }).execute()

        if not events:
            print("No upcoming events found.")
            return

        # Prints the start and name of the next 10 events
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            print(start, event["summary"])

    except HttpError as error:
        print("An error occurred: %s" % error)


def renew_url():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)

        now = datetime.datetime.now()

        # Add a week to the current date and time
        one_week_from_now = now + datetime.timedelta(weeks=1)

        # Convert the resulting datetime object to milliseconds
        milliseconds = int(one_week_from_now.timestamp() * 1000)


        xd = (
            service.events()
            .watch(
                calendarId="primary",
                body={
                    "id": "choach_uniq_id3422",
                    "type": "web_hook",
                    "address": "https://c503-85-214-57-62.ngrok-free.app/calupdates",
                    "expiration": milliseconds,
                },
            )
            .execute()
        )

    except HttpError as error:
        print("An error occurred: %s" % error)


def get_gc_service():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)

        return service

    except HttpError as error:
        print("An error occurred: %s" % error)

        return None


def get_gc_events(service):
    if service is None:
        return []
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    print("Getting the upcoming 10 events")
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=20,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    return events


def get_events_at_day(service, day_str):
    if service is None:
        return []
    # Call the Calendar API
    date_obj = datetime.datetime.strptime(day_str, "%d.%m.%Y")
    utc_date_obj = date_obj.astimezone(pytz.utc)

    next_day = utc_date_obj + datetime.timedelta(days=1)

    time_min = utc_date_obj.isoformat() # 'Z' indicates UTC time
    time_max = next_day.isoformat()  # 'Z' indicates UTC time

    print("Getting the upcoming 20 events")
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=time_min.replace("+00:00", "Z"),
            timeMax=time_max.replace("+00:00", "Z"),
            maxResults=20,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    str_list = []

    for event in events:
        start = datetime.datetime.fromisoformat(event['start']['dateTime']).strftime("%H:%M")
        end = datetime.datetime.fromisoformat(event['end']['dateTime']).strftime("%H:%M")
        str_list.append(start + " - " + end)

    return ", ".join(str_list)


def add_event(service, day_str, time_str, dur_str, title, decr=""):

    start_obj = datetime.datetime.strptime(day_str + " " + time_str, "%d.%m.%Y %H:%M:%S")

    end_obj = start_obj + datetime.timedelta(minutes=int(dur_str))

    event = {
        'summary': title,
        'description': decr,
        'start': {
            'dateTime': start_obj.isoformat(),
            'timeZone': "Europe/Berlin",
        },
        'end': {
            'dateTime': end_obj.isoformat(),
            'timeZone': 'Europe/Berlin',
        },
        'reminders': {
            'useDefault': True,
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()

# 
#
if __name__ == "__main__":
    # main()
    # get_gc_events(get_gc_service())
    # print(get_events_at_day(get_gc_service(), "18.09.2023"))
    add_event(get_gc_service(), "18.09.2023", "12:00:00", "30", "test")
