x = input()
print(f"Upper: {len(list(filter(lambda i: i == i.upper(), x)))}\nLower: {len(list(filter(lambda i: i == i.lower(), x)))}")