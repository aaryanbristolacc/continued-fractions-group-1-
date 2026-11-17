# Need to make two functions
# One that computes the continued fraction
# One that reconstructs a rational number from its continued fraction
# Then analyse and test the functions

import math
import time

# First function
def continued_fraction(theta, n):
    cf = []
    theta_i = theta

    for i in range(n+1):
        # Define a as required in question
        a = math.floor(theta_i)
        cf.append(a)

        remainder = theta_i - a

        # Stop the loop if its an exact integer (a = theta)
        if abs(remainder) < 1e-15:
            break

        theta_i = 1 / remainder

    return cf

# Second function
def reconstructed_rational(cf):
    if not cf:
        return 0

    # Begin fraction
    fraction = cf[-1] / 1

    # Work backwards through a
    for a in reversed(cf[:-1]):
        fraction = a + (1 / fraction)
        
    return fraction

# Now to test and analyse
# Test with rational number
cf_rational = continued_fraction(4/5, n = 10)
print("4/5 expanded is :", cf_rational)

# Test with Irrational (root 5)
cf_irrational = continued_fraction(math.sqrt(5), n = 10)
print("Root 5 expanded is :", cf_irrational)
print("Root 5 reconstructed is :", reconstructed_rational(cf_irrational))

# Analysis
# Execution time
t0 = time.perf_counter()
cf = continued_fraction(math.sqrt(5), n=10)
t_cf = (time.perf_counter() - t0) * 1e6

t0 = time.perf_counter()
frac = reconstruct_rational(cf)
t_rec = (time.perf_counter() - t0) * 1e6

print(f"continued_fraction time: {t_cf:.2f} microseconds")
print(f"reconstruct_rational time: {t_rec:.2f} microseconds")

# Hence our reconstructed function is faster
