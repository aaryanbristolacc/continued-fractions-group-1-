# Continued Fraction Lengths
from math import gcd
from collections import Counter

import numpy as np
import matplotlib.pyplot as plt


# Generate all reduced fractions a/q with 0 < a < q <= Q.
# Store fractions exactly as numerator-denominator pairs.
def core4_fractions(Q):
    if Q < 2:
        raise ValueError("Q must be at least 2.")

    for q in range(2, Q + 1):
        for a in range(1, q):
            if gcd(a, q) == 1:
                yield a, q


# Return [a1, ..., ak] for a/q = [0; a1, ..., ak].
def core4_coefficients(a, q):
    if not 0 < a < q:
        raise ValueError("Require 0 < a < q.")

    coefficients = []

    while a != 0:
        coefficient, remainder = divmod(q, a)
        coefficients.append(coefficient)
        q, a = a, remainder

    return coefficients


def core4_length(a, q):
    return len(core4_coefficients(a, q))


def core4_fibonacci(n):
    a, b = 0, 1

    for _ in range(n):
        a, b = b, a + b

    return a


# Check a few known examples.
assert core4_coefficients(1, 2) == [2]
assert core4_coefficients(2, 3) == [1, 2]
assert core4_coefficients(3, 5) == [1, 1, 2]
assert core4_coefficients(5, 8) == [1, 1, 1, 2]

print("The example checks passed.")

## Minimum denominator for a given length
# Search in increasing denominator order.
def core4_minimum_denominators(Q):
    minimums = {}

    for a, q in core4_fractions(Q):
        k = core4_length(a, q)

        if k not in minimums:
            minimums[k] = (a, q)

    return minimums


search_Q = 200
minimums = core4_minimum_denominators(search_Q)

print("Length | Example fraction | Minimum denominator | Fibonacci prediction")

for k in sorted(minimums):
    a, q = minimums[k]
    predicted = core4_fibonacci(k + 2)

    print(f"{k:6d} | {a:3d}/{q:<11d} | {q:19d} | {predicted:20d}")

    assert q == predicted
    assert core4_coefficients(a, q) == [1] * (k - 1) + [2]
