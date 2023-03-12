from __future__ import print_function
import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build

def get_calendar_service(api_key_path):
    """Создает объект сервиса для доступа к Google Calendar API с помощью API-ключа"""
    credentials     = service_account.Credentials.from_service_account_file(api_key_path)
    return build('calendar', 'v3', credentials=credentials)

def check_event_exists(calendar_service, event_title):
    """Проверяет наличие события в календаре"""
    start_date      = datetime.datetime.utcnow().isoformat() + 'Z'
    end_date        = (datetime.datetime.utcnow() + datetime.timedelta(days=1)).isoformat() + 'Z'

    events_result   = calendar_service.events().list(calendarId='primary', timeMin=start_date,
                                                   timeMax=end_date, singleEvents=True,
                                                   orderBy='startTime').execute()
    events          = events_result.get('items', [])

    for event in events:
        if event['summary'] == event_title:
            return True

    return False

def add_event_to_calendar(calendar_service, event_title, event_description, start_time, end_time, timezone='Asia/Tbilisi', color_id=5):
    """Добавляет событие в календарь"""
    event           = {
                        'summary': event_title,
                        'description': event_description,
                        'start': {
                            'dateTime': start_time,
                            'timeZone': timezone,
                        },
                        'end': {
                            'dateTime': end_time,
                            'timeZone': timezone,
                        },
                        'colorId': str(color_id)
                    }
    event           = calendar_service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))