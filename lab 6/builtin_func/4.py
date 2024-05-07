from time import sleep
from math import sqrt
value = int(input())
time = int(input("Write a sleep time in ms "))
sleep(time/1000)
print(f"Square root of {value} after {time} miliseconds is {sqrt(value)}")