x = list(map(str, input().split()))
with open("output.txt", 'w') as a:
    a.write("\n".join(x))
a.close()