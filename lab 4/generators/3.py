def gena(N):
    i = 0
    while i < N:
        if (i % 3 == 0 or i % 4 == 0): yield i
        i += 1
print(list(i for i in gena(int(input()))))