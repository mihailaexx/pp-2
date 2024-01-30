def gena(N):
    i = N
    while i > -1:
        yield i
        i -= 1
print(list(i for i in gena(int(input()))))