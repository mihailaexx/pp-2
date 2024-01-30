import datetime
x = datetime.datetime.now().replace(microsecond=0)
print(x)
# or
# print(x.strftime("%d-%m-%Y %H:%M:%S"))