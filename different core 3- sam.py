import numpy as np
import random
from math import gcd, isqrt, log


def sample_fractions(Q, N):
    fractions = []

#1 on first line, 2 on next... , and the total is just sum of all the lines. (single slash gives float not integer as well.)
    total = Q * (Q - 1) // 2

    while len(fractions) < N:

        r = random.randrange(total)

#isqrt is sqrt and then rounded down#
#this line and for a as well from ai so change if needed- lwk spent way too much time on it and couldnt work it out-#
#turns list from 0, 12, 345, ... into denominator#
        q = (1 + isqrt(1 + 8*r)) // 2 + 1

        first = (q - 2) * (q - 1) // 2
        a = r - first + 1

        if gcd(a, q) == 1:
            fractions.append((a, q))

    return fractions











def cf_length(a, q):
#this is for the s1(x)#
    length = 0

#Euclidean algorithm without needing to use part 1 (using question 4)#
    while a != 0:
        a, q = q % a, a      # a/q -> q/a (->) (qmod(a))/a#
        length += 1  

    return length





def gm(a, q):
    p = 0
    while a > 0:
        p += log(a / q) 
        a, q = q % a, a      
    return p








def calculate_S(fractions):

    S_one = []
    S_log = []

    for a, q in fractions:

# phi(x) = 1#
        S_one.append(cf_length(a, q))

# phi(x) = log(1/x)#
        S_log.append(gm(a, q))

    return np.array(S_one), np.array(S_log)








Q_values = [10**2, 10**3, 10**4, 10**5, 10**6]

mean_one = []
variance_one = []
means_log = []
variances_log = []


for Q in Q_values:

    fractions = sample_fractions(Q, 50000)

    S_one, S_log = calculate_S(fractions)

#for phi=1
    mu_one = np.mean(S_one)
    var_one = np.mean((S_one - mu_one)**2)

    mean_one.append(mu_one)
    variance_one.append(var_one)

#for phi = log...#
    mu_log = np.mean(S_log)
    var_log = np.mean((S_log - mu_log)**2)

    means_log.append(mu_log)
    variances_log.append(var_log)






for i, Q in enumerate(Q_values):

    print("\nQ =", Q)

    print("phi = 1:")
    print("Mean =", mean_one[i])
    print("Variance =", variance_one[i])

    print("phi = log(1/x):")
    print("Mean =", means_log[i])
    print("Variance =", variances_log[i])




#might be useful to use every fraction if its for a low number instead of just a sample, so:
#def all_fractions(Q):
#    fractions = []
#
#    for q in range(2, Q + 1):
#        for a in range(1, q):
#            if gcd(a, q) == 1:
#                fractions.append((a, q))
#
#     return fractions        #
#could compute this




#The samples are chosen uniformly as all N(n-1)/2 fractions minus the double counted such as 1/2 to 2/4 are accounted for, which is all the fractions in the group. Then when the set is made of all these, the sample is randomly picked from that set, thus ensuring completly unbiased random set. (The ones picked that arent from the set are quikly filtered out by the conditions that are set for the group.)











#4. 

#This takes the form of the fibbonacci sequence. This is because: instead of looking for smallest k, look for the largest l for 1,2,3,4... . Here you find that the subsequent phases of the algorithm use smaller numbers that are previous.#
#This therefore means that to find the smallest number, the second line of working must be the smallest number for the number below and so on.#
#Taking the form of k=1*(k-1)+(k-2), where k is the term of the fibbonacci k-1 is the one before and k-2 is the one before that. It is multiplied by 1 as there is symmetry for both sides and thus using 2 or 3 wouldnt make a larger number of steps#
#This would make the next line (k-1)=1*(k-2)+(k-3)... . This is now the optimal result for the number below and as one line of working has been used up, that makes it the optimal result for that value of k.

#Therefore for the smallest denominator, take k.....


def fib(n):
    a, b = 1, 2          #values for n=0 and n=1#
    for p in range(n - 1):
        a, b = b, a + b
    return b

print(fib(6))
