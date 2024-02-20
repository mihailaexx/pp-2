# multiply to exact value
x = [int(x) for x in input().split()]
n = int(input())
print(list(map(lambda x: x*n, x)))

# multiply numbers in array between each others
i = 1
for num in x:
    i *= num
print(i)