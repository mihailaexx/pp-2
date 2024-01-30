def gena(N):
    i = 0
    while i < N:
        if i % 2 == 0: yield i
        i+=1
print(*list(i for i in gena(int(input()))), sep=", ")