import checl_rdp_attack
from datetime import datetime

events = checl_rdp_attack.get_events()



current_datetime = datetime.now()
current_time = current_datetime.strftime("%H:%M:%S")

# print(current_time)





from datetime import time

# times = [time(11, 55, 35), time(10, 54, 35), time(11, 24, 35), time(9, 54, 35), time(11, 54, 25), time(12, 54, 35), time(21, 54, 35), time(11, 54, 35)]
# times = []
# for i in events:
#     # print(i.date)
#     times.append(i.time)


def get_times_future_or_equal(date_time_now):
    # target_time = time.fromisoformat(date_time_now)
    # return [t for t in times if t >= target_time]
    events_new = []
    
    d = date_time_now.day
    mo = date_time_now.month
    y = date_time_now.year

    h = date_time_now.hour
    m = date_time_now.minute
    s = date_time_now.second
    date_time_now = datetime(y,mo,d,h,m,s)

    for event in events:
        event_date_time = datetime(event.year,event.month,event.day,event.time.hour,event.time.minute,event.time.second)
        
        # если событие новое или текущее
        if event_date_time > date_time_now or event_date_time == date_time_now:
            events_new.append(event)
    return events_new 
# 22.11.2023 6:44:37
final_events = get_times_future_or_equal(datetime(2023,11,22,6,42,49))
for i in final_events:
    print(i.name + "\n" + str(i.ip) + "\n\n")
print(len(final_events))

# target_time_str = "11:54:35"
# result = get_times_after_or_equal(current_time)
print("\n")
# print(len(result))
# print(time(11, 55, 35).strftime("%H:%M:%S"))

from datetime import datetime, timedelta

def count_ip_events(ip_address, event_list):

    # тут указываем до какого момента проверить количество попыток 
    # current_time = datetime.now() #текущее вермя
    current_time = datetime(2023, 11, 16, 14, 45, 42)
    
    # интервал запрета
    interval = {
        "hour": 1,
        "mimute": 3,
        "second": 0
    }
    one_hour_ago = current_time - timedelta(hours=interval["hour"], minutes=interval["mimute"], seconds=interval["second"])

    count = 0
    for event in event_list:
        event_date_time = datetime(event.year,event.month,event.day,event.time.hour,event.time.minute,event.time.second)
        if event.ip == ip_address and event_date_time >= one_hour_ago and event_date_time <= current_time:
            count += 1
    
    return count
# print(count_ip_events("202.55.135.11", events))
diapazone = timedelta(hours=1)
# events_data_default = {
#     "name": "",
#     "last": None,
#     "count": None,
#     "max": 0
# }
def get_events_diapazone(diapazone):
    events_counts = {}
    # time_count = 0
    for event in events:
        event_date_time = datetime(event.year,event.month,event.day,event.time.hour,event.time.minute,event.time.second)
        # name = event.name
        if event.ip not in events_counts:
            event_data = {}
            event_data["name"] = event.name
            event_data["last"] = event_date_time
            event_data["count"] = 1
            event_data["max"] = 1
            events_counts[event.ip] = event_data
        else:
            last = events_counts[event.ip]["last"]
            result = last - event_date_time
            
            # если час еще не прошел
            if result<=diapazone:
                events_counts[event.ip]["count"] += 1

                # если счетчик выше чем рекорд то ставим новый рекорд
                if events_counts[event.ip]["count"] > events_counts[event.ip]["max"]:
                    events_counts[event.ip]["max"] = events_counts[event.ip]["count"]
            else:
                events_counts[event.ip]["last"] = event_date_time
                event_data["count"] = 1
    return events_counts
# for event in get_events_diapazone():
    
# def get_list_addresses_diapazone():
#     addresses = []
#     rule = find_firewall_rule_by_name(rule_name)

#     if rule is not None:
#         remote_addresses = rule.RemoteAddresses.split(",") if rule.RemoteAddresses else []
#         # print(f"Удаленные IP-адреса для правила '{rule_name}':")
#         for address in remote_addresses:
#             # print(address.strip()) 
#             addresses.append(address.strip()) 
#     else:
#         print(f"Правило '{rule_name}' не найдено.")
#     return addresses