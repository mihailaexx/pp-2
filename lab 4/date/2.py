import datetime
x = datetime.date.today()
print(f"Yesterday: {x - datetime.timedelta(days=1)}\nToday: {x}\nTomorrow: {x + datetime.timedelta(days=1)}")
# or
# print(f"Yesterday: {x.day-1}.{x.month}.{x.year}\nToday: {x.day}.{x.month}.{x.year}\nTomorrow: {x.day+1}.{x.month}.{x.year}")