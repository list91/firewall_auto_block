import checl_rdp_attack
from datetime import datetime, timedelta
import firewall
import time
time1 = time.time()

events = checl_rdp_attack.get_events()

# max_count = 5
h = int(input("Ведите количество часов котрое охватывает диапазон: "))
max_count = int(input("Ведите максимальное количество попыток подключений в заданный диаппазон: "))
print("\n")
diapazone = timedelta(minutes=h)

def get_events_diapazone(diapazone):
    events_counts = {}
    for event in events:
        event_date_time = datetime(event.year,event.month,event.day,event.time.hour,event.time.minute,event.time.second)
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

# print("ЗАБЛОКИРОВАТЬ:")
arr = get_events_diapazone(diapazone)
ip_black_list = []

for event in arr:
    # print(event)
    if arr[event]["max"] >= max_count:
        # print(arr[event]["name"])
        # print(event)
        ip_black_list.append(event)
        # print("")

ips_firewall = firewall.get_list_addresses_firewall()
for ip in ip_black_list:
    is_created = False
    for ip_firewall in ips_firewall:
        if ip == ip_firewall:
            is_created = True
            # print(str(ip)+" УЖЕ ВНЕСЕН")
        # else:
            # print(str(ip)+" НУЖНО ВНЕСТИ  ----------")
    if is_created:
        print(str(ip)+" - УЖЕ ВНЕСЕН")
    else:
        print(str(ip)+" - НУЖНО ВНЕСТИ  !!!!!!!!!!!!!")

time2 = time.time()