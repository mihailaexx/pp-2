import datetime
x = datetime.date.today()
print(x - datetime.timedelta(days=5))
# or
# print(f"{x.day-5}-{x.month}-{x.year} was 5 days from today")