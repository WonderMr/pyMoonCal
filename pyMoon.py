import os.path

import ephem
import datetime
import numpy as np
import cal
import loc

# Определяем текущие координаты и время
observer                        = ephem.Observer()
lon, lat                        = loc.getLoc()
observer.lon                    = np.deg2rad(lon)
observer.lat                    = np.deg2rad(lat)
observer.elevation              = 60 # Высота над уровнем моря (в метрах)
now                             = datetime.datetime.utcnow()

# Создаем объект PyEphem для расчета лунных данных
moon                            = ephem.Moon()
moon.compute(observer)
start_next_mmonth               = ephem.localtime(ephem.next_new_moon(now))
start_prev_mmonth               = ephem.localtime(ephem.previous_new_moon(now))
print("Moon month starts: ", start_prev_mmonth)
print("Moon month ens: ", start_next_mmonth)
c_date                          = start_prev_mmonth
md_num                          = 0
mdays                           = {}
while c_date < start_next_mmonth:
    c_date                      = c_date + datetime.timedelta(hours=1)
    observer.date               = c_date
    md_num                      = md_num + 1
    # Расчитываем лунный день
    rise                        = ephem.localtime(observer.previous_rising(ephem.Moon()))
    c_date                      = ephem.localtime(observer.next_rising(ephem.Moon()))
    #print("Moon day: ", md_num, " starts at: ", rise)
    mdays[md_num]               = [rise, c_date]

# Создаем объект для работы с Google Calendar API
api_key_path                    = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".keys\\client_secret.json")
calendar_service                = cal.get_calendar_service(api_key_path)

for mday in mdays[0:1]:
    # Данные для события
    event_title                 = f"Moon Day {mday}"
    event_description           = ''
    start_time                  = mdays[mday][0]
    end_time                    = mdays[mday][1]
    timezone                    = 'Asia/Tbilisi'
    color_id                    = 5

    # Проверяем наличие события в календаре и добавляем его, если его нет
    if not cal.check_event_exists(calendar_service, event_title):
        cal.add_event_to_calendar(calendar_service, event_title, event_description, start_time, end_time, timezone,
                              color_id)
    else:
        print('Event already exists')
