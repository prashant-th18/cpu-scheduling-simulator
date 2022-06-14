from src.utils.process import Process
import random

processes = []

n = 7
burst = 10
priority = 5


def rand_num(num):
    return random.randint(1, num)


# To ensure that first process arrives at time 0
processes.append(Process(0, 0, rand_num(burst), rand_num(priority)))

for i in range(1, n):
    p = Process(i, rand_num(n), rand_num(burst), rand_num(priority))
    processes.append(p)


"""
This file is responsible for creating small random tests
"""
