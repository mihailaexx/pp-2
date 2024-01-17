from itertools import permutations 
a = str(input())
b = permutations(a)
for row in list(b):
    print(*row)