import datetime
x = datetime.date.today()
y = datetime.date(*list(map(int, input("Input \"year month day\": ").split())))
print(f"Days between today and {y}: {x-y}")