from __future__ import print_function
from collections import defaultdict

import datetime
import os.path

import pytz

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]


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
    # print("Getting the upcoming 10 events")
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
        if "[COACH]" in event["summary"]:
            continue
        start = datetime.datetime.fromisoformat(event['start']['dateTime']).strftime("%H:%M")
        end = datetime.datetime.fromisoformat(event['end']['dateTime']).strftime("%H:%M")
        str_list.append(start + " - " + end)

    # return ", ".join(str_list)
    return str_list


def get_events_at_days(service, day_str=None, n_days=7):
    
    if day_str is None:
        now = datetime.datetime.now()
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        day_str = today.strftime("%d.%m.%Y")

    events_day_dict = {}

    for i in range(n_days):
        date_obj = datetime.datetime.strptime(day_str, "%d.%m.%Y")
        date_obj += datetime.timedelta(days=i)
        new_day_str = date_obj.strftime("%d.%m.%Y")

        events_day_dict[new_day_str] = get_events_at_day(service, new_day_str)

    return events_day_dict




def add_event(service, day_str, time_str, dur_str, title, decr=""):

    start_obj = datetime.datetime.strptime(day_str + " " + time_str, "%d.%m.%Y %H:%M")

    end_obj = start_obj + datetime.timedelta(minutes=int(dur_str))

    event = {
        'summary': "[COACH] " + title,
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


def clear_coach_events(service):
    events = get_gc_events(service)

    for event in events:
        if "[COACH]" in event["summary"]:
            service.events().delete(calendarId='primary', eventId=event["id"]).execute()




def compare_events(gc_events, workouts):

    workout_day_dict = defaultdict(list)

    for workout in workouts:
        wday = workout['date']
        wdatetime = datetime.datetime.strptime(workout['date'] + " " + workout['start_time'], "%d.%m.%Y %H:%M")
        wdatetime_end = wdatetime + datetime.timedelta(minutes=int(workout['duration']))

        workout_day_dict[wday].append((wdatetime, wdatetime_end))

    for eday, events in gc_events.items():
        for event in events:
            edatetime = datetime.datetime.strptime(eday + " " + event.split(" - ")[0], "%d.%m.%Y %H:%M")
            edatetime_end = datetime.datetime.strptime(eday + " " + event.split(" - ")[1], "%d.%m.%Y %H:%M")

            for wdatetime, wdatetime_end in workout_day_dict[eday]:
                if wdatetime < edatetime < wdatetime_end or wdatetime < edatetime_end < wdatetime_end:
                    print("Conflict: ", wdatetime, wdatetime_end, " - ", edatetime, edatetime_end)
                    return False

    return True


# 
#
if __name__ == "__main__":
    # get_gc_events(get_gc_service())
    # print(get_events_at_day(get_gc_service(), "18.09.2023"))
    # print(get_events_at_days(get_gc_service()))
    add_event(get_gc_service(), "18.09.2023", "14:00", "120", "test")
    # clear_coach_events(get_gc_service())
