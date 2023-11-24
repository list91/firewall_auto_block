import win32evtlog
def write_test0():
    # Открываем журнал безопасности Windows
    hand = win32evtlog.OpenEventLog(None, 'Security')

    # Определяем стартовую позицию чтения журнала
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ
    total = win32evtlog.GetNumberOfEventLogRecords(hand)

    # Читаем записи из журнала
    count = 0
    out_file = open("out.txt", "w", encoding="utf-8")
    while True:
        events = win32evtlog.ReadEventLog(hand, flags, 0)
        
        # Проверяем, есть ли записи
        if events:
            for event in events:
                if event.EventID == 4625:
                    count+=1
                    # Выводим информацию о записи
                    out_file.write('Event Category:'+ str(event.EventCategory)+"\n")
                    out_file.write('Time Generated:'+ str(event.TimeGenerated)+"\n")
                    out_file.write('Source Name:'+ str(event.SourceName)+"\n")
                    out_file.write('Event ID:'+ str(event.EventID)+"\n")
                    out_file.write('Event Type:'+ str(event.EventType)+"\n")
                    out_file.write('Event String:'+ str(event.StringInserts)+"\n")
                    out_file.write('-' * 50+"\n")
                    print(str(event.TimeWritten) + "event.TimeWritten")
                    print(str(event.ClosingRecordNumber) + "event.ClosingRecordNumber")
                    print(str(event.ComputerName) + "event.ComputerName")
                    print(str(event.Data) + "event.Data")
                    print(str(event.RecordNumber) + "event.RecordNumber")
                    print(str(event.Reserved) + "event.Reserved")
                    print(str(event.ReservedFlags) + "event.ReservedFlags")
                    print(str(event.Sid) + "event.Sid")
                    print(str(event.TimeGenerated) + "event.TimeGenerated")
                    print("\n\n")
        else:
            break

    # Закрываем журнал безопасности
    out_file.close()
    print(count)
    win32evtlog.CloseEventLog(hand)
def get_events():
    # Открываем журнал безопасности Windows
    hand = win32evtlog.OpenEventLog(None, 'Security')

    # Определяем стартовую позицию чтения журнала
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ
    total = win32evtlog.GetNumberOfEventLogRecords(hand)
    event_list = []

    while True:
        events = win32evtlog.ReadEventLog(hand, flags, 0)
        
        # Проверяем, есть ли записи
        if events:
            for event in events:
                if event.EventID == 4625:
                    event_object = Event(
                        event.StringInserts[5],
                        event.StringInserts[19],
                        event.TimeWritten.hour, 
                        event.TimeWritten.minute, 
                        event.TimeWritten.second,
                        event.TimeWritten.day,
                        event.TimeWritten.month,
                        event.TimeWritten.year
                    )
                    event_list.append(event_object)

        else:
            break

    win32evtlog.CloseEventLog(hand)
    return event_list

import datetime

def write_test():
    # Открываем журнал безопасности Windows
    hand = win32evtlog.OpenEventLog(None, 'Security')

    # Определяем стартовую позицию чтения журнала
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    total = win32evtlog.GetNumberOfEventLogRecords(hand)

    # Получаем текущую дату и время
    now = datetime.datetime.now()

    # Вычисляем время 12 часов назад
    twelve_hours_ago = now - datetime.timedelta(hours=12)

    # Читаем записи из журнала
    count = 0
    out_file = open("out.txt", "w", encoding="utf-8")
    while True:
        events = win32evtlog.ReadEventLog(hand, flags, 0)

        # Проверяем, есть ли записи
        if events:
            for event in events:
                # Проверяем, что время генерации записи находится в пределах последних 12 часов
                if event.TimeGenerated >= twelve_hours_ago:
                    count += 1
                    # Выводим информацию о записи
                    out_file.write('Event Category:' + str(event.EventCategory) + "\n")
                    out_file.write('Time Generated:' + str(event.TimeGenerated) + "\n")
                    out_file.write('Source Name:' + str(event.SourceName) + "\n")
                    out_file.write('Event ID:' + str(event.EventID) + "\n")
                    out_file.write('Event Type:' + str(event.EventType) + "\n")
                    out_file.write('Event String:' + str(event.StringInserts) + "\n")
                    out_file.write('-' * 50 + "\n")
                    print(str(event.TimeWritten) + "event.TimeWritten")
                    print(str(event.ClosingRecordNumber) + "event.ClosingRecordNumber")
                    print(str(event.ComputerName) + "event.ComputerName")
                    print(str(event.Data) + "event.Data")
                    print(str(event.RecordNumber) + "event.RecordNumber")
                    print(str(event.Reserved) + "event.Reserved")
                    print(str(event.ReservedFlags) + "event.ReservedFlags")
                    print(str(event.Sid) + "event.Sid")
                    print(str(event.TimeGenerated) + "event.TimeGenerated")
                    print("\n\n")
        else:
            break

    # Закрываем журнал безопасности
    out_file.close()
    print(count)
    win32evtlog.CloseEventLog(hand)

class Event():
    def __init__(self, name, ip, h, m, s, d, mo, y):
        self.name = name
        self.ip = ip
        self.time = datetime.time(h,m,s)
        self.day = d
        self.month = mo
        self.year = y
