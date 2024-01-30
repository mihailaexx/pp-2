# немного не понял задание, нужно квадраты до н или н квадратов????
def gena(N):
	i = 0
	while i**2 < N:
		yield i**2
		i += 1
# def gena(N):
# 	i = 0
# 	while i < N:
# 		yield i**2
# 		i += 1
print(*list(i for i in gena(int(input()))))