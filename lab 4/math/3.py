from math import tan, pi
n = int(input("Input number of sides "))
lenght = int(input("Input lenght of a side "))
apothem = lenght / (2 * round(tan(pi/n)))
print((n*lenght*apothem)/2)