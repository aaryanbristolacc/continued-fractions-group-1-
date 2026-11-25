#extension work - task 7


#making the function to compute the frequency

"""
to declutter what the notation is saying in words its asking for the cardinality of the set of ordered pairs of
(x,j) such that x is an array taken from the random sample of f_Q and j is an index in in the array of x such that
a_j  = k, where k is our input parameter and then we divide this expression by the sum of the lengths from all x in
the random sample
"""

#this function uses logic defined in the previous sections such as:
#the continued fraction function is defined in core 1
#the random sample and f_Q logic is defined in core 3
#ill copy them over as a comment just so that you dont have to scroll back up

#start of copied code


#imports
import math
import random
import matplotlib.pyplot as plt
from fractions import Fraction # eliminates floating point errors

#exact version of continued fractions (always terminates for rational theta)
def continued_fraction(theta):
    cf = []

    while theta != 0:
        a = math.floor(theta)
        cf.append(a)

        remainder = theta - a

        if remainder == 0:
            break

        theta = 1 / remainder

    return cf

def f_Q(Q):
    f_Q = []
    for q in range(2,Q+1):
        for a in range(1,q):
            if math.gcd(a,q) == 1:
                f_Q.append(Fraction(a,q))
    return f_Q 

def random_sample(fq_size, sample_size):
    return random.sample(f_Q(fq_size), sample_size)

#end of copied code

A = random_sample(10000, 1000) #creates random sample

#implementation for p(k) function
def p(k,A):
    sum_length_x = 0 # initialises the sum of lengths of x (denominator)
    counter= 0 # counts how many times k appears (numorator)
    for x in A:
        cf = continued_fraction(x)
        
        sum_length_x += len(cf)
        for j in range(len(cf)):
            if cf[j] == k:
                counter += 1
    return counter/sum_length_x 

#the plot of p(k) against k

k_values = range(1, 20)
p_values = [p(k, A) for k in k_values]

plt.figure(figsize=(10, 6))

plt.plot(k_values, p_values, marker='o')

plt.xlabel("k values")
plt.ylabel("p(k) values")
plt.title("Plot of p(k) values against k")

plt.xticks(list(k_values))
plt.grid(True, alpha=0.3)

plt.show()

