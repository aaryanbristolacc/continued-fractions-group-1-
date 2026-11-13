#core 3 
import * from math
import random

#set construction for rationals - this can probably be optimised but good enough for now
def f_Q(Q):
    f_Q = []
    for q in range(Q+1):
        for a in range(0,q):
            if gcd(a,q) == 1:
                f_Q.append(a/q)
    return f_Q 


#gauss map function definition:
def T(x):
    if 0 < x and x <1:
        return 1/x - floor(1/x)
    elif x ==0:
        return 0
    else:
        raise ValueError(" x not in [0,1) ") # detect erronious input

#phi function definition:
def phi(x):
    return log(floor(1/x))

#S_phi fuction definition
def S_phi(cf_approx):
    result = None
    for i in range(len(cf_approx)):
        result += phi(pow(T(cf_approx[i]),i-1))

#random sample
sample_size  = 67 # they didnt specify a size
F32 = f_Q(32) # create set
A = random.sample(F32, sample_size) # create sample

#will do the rest later after talking with others on friday
#github acting up for some reason so couldnt commit
    
