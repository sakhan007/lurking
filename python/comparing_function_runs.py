"""
This code is copied from

https://stackoverflow.com/questions/6800193/what-is-the-most-efficient-way-of-finding-all-the-factors-of-a-number-in-python

I wanted to learn how to compare different algorithims

"""
import timeit
from math import sqrt
from matplotlib.pyplot import plot, legend, show
from functools import reduce

def factors_1(n):
    return set(reduce(list.__add__,
                ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))

def factors_2(n):
    step = 2 if n%2 else 1
    return set(reduce(list.__add__,
        ([i,n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0 )))

x = range(1, int(1e6), 1000)
y = []
for i in x:
    f_1 = timeit.timeit("factors_1({})".format(i), setup = 'from __main__ import factors_1', number = int(1e4))
    f_2 = timeit.timeit('factors_2({})'.format(i), setup = 'from __main__ import factors_2', number = int(1e4))
    y.append(f_1/f_2)
plot(x,y, label = 'Run time with/without parity check')
legend()
show()



