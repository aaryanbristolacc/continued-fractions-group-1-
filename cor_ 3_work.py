#core 3 
import math
import random
from fractions import Fraction

#set construction for rationals - this can probably be optimised but good enough for now
def f_Q(Q):
    f_Q = []
    for q in range(2,Q+1):
        for a in range(1,q):
            if math.gcd(a,q) == 1:
                f_Q.append(Fraction(a,q))
    return f_Q 


#gauss map function definition:
def T(x):
    if 0 < x and x <1:
        return 1/x - math.floor(1/x)
    elif x ==0:
        return 0
    else:
        raise ValueError(" x not in [0,1) ") # detect erronious input

#phi function definition:
def phi(x):
    return math.log(math.floor(1/x))

#S_phi fuction definition
def S_phi(cf_approx):
    result = 0
    for i in range(len(cf_approx)):
        result += phi(pow(T(cf_approx[i]),i-1))

#random function sample

def random_sample(fq_size, sample_size):
    return random.sample(f_Q(fq_size), sample_size)
    
sample_size  = 67 # they didnt specify a size
A = random_sample(32, sample_size) # create sample

#will do the rest later after talking with others on friday
#github acting up for some reason so couldnt commit
#another group member finished this bit
