# Core 4: Continued Fraction Lengths
#
# For a reduced fraction x = a/q in (0, 1), we use its canonical continued fraction expansion:
# x = [0; a1, ..., ak], where ak >= 2.
#
# The length is ell(x) = k. The initial coefficient a0 = 0 is not counted.
# We use the Euclidean algorithm with integer arithmetic. This avoids rounding errors when calculating the coefficients.

from math import gcd
from collections import Counter

import numpy as np
import matplotlib.pyplot as plt

# 1. Basic functions
# Generate reduced fractions in (0, 1) as (numerator, denominator) pairs.
def core4_fractions(Q):
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

# The length is the number of steps in the Euclidean algorithm.
def core4_length(a, q):
    return len(core4_coefficients(a, q))

# Return the Fibonacci number F_n, with F_0 = 0 and F_1 = 1.
def core4_fibonacci(n):
    a, b = 0, 1

    for _ in range(n):
        a, b = b, a + b

    return a

# 2. Minimum denominator for each length

# Let d_k be the smallest denominator of a rational number in (0, 1) with canonical continued fraction length k.
# The convergent denominators satisfy:
# q_{-1} = 0, q_0 = 1, q_j = a_j * q_{j-1} + q_{j-2}.
# For an expansion of length k, we have:
# a_j >= 1 for 1 <= j < k, a_k >= 2.
# The denominator cannot decrease when a coefficient increases.
# Therefore, the minimum is attained by choosing:
# a_1 = ... = a_{k-1} = 1, a_k = 2.
# For k = 1, the minimum denominator is 2, attained by [0; 2].
# For k >= 2, the coefficients before the final term give
# q_j = F_{j+1} for 0 <= j <= k-1. Hence:
# d_k = 2 * F_k + F_{k-1} = F_{k+2}.
# The sequence is:
# d_1, d_2, d_3, ... = 2, 3, 5, 8, 13, 21, ...
# A fraction attaining this minimum is F_{k+1}/F_{k+2}, whose coefficients are k-1 ones followed by a final 2.
#
# The search below checks this formula for the lengths found with denominators at most 200. The proof above applies to all k.

def core4_minimum_denominators(Q):
    minimums = {}

    for a, q in core4_fractions(Q):
        k = core4_length(a, q)

        if k not in minimums:
            minimums[k] = (a, q)

    return minimums

minimums = core4_minimum_denominators(200)

print("Length | Minimum denominator | Fibonacci prediction")

for k in sorted(minimums):
    a, q = minimums[k]
    predicted = core4_fibonacci(k + 2)

    print(k, q, predicted)
    assert q == predicted

# 3. Distribution of lengths

# Enumerate all reduced fractions 0 < a < q <= Q.
# c_Q(k) counts fractions of length k.
# P_Q(k) = c_Q(k) / total number of fractions.
#
# We use the full set, so there is no sampling error.
# Moderate Q values keep the computation manageable.


def core4_distribution(Q):
    counts = Counter()

    for a, q in core4_fractions(Q):
        counts[core4_length(a, q)] += 1

    total = sum(counts.values())
    ks = np.arange(1, max(counts) + 1)

    frequencies = np.array(
        [counts.get(int(k), 0) for k in ks]
    )
    probabilities = frequencies / total

    mean = np.sum(ks * probabilities)
    variance = np.sum((ks - mean)**2 * probabilities)

    return {
        "Q": Q,
        "ks": ks,
        "counts": frequencies,
        "probabilities": probabilities,
        "total": total,
        "mean": mean,
        "sd": np.sqrt(variance),
        "max_length": int(ks[-1])
    }


Q_values = [20, 50, 100, 200]
results = [core4_distribution(Q) for Q in Q_values]

# Summary table
print(" Q  | Number of fractions | Mean length | Standard deviation | Max length")

for result in results:
    print(
        f"{result['Q']:3d} | "
        f"{result['total']:19d} | "
        f"{result['mean']:11.4f} | "
        f"{result['sd']:18.4f} | "
        f"{result['max_length']:10d}"
    )

# 4. Plot the length distributions
fig, axes = plt.subplots(
    2, 2, figsize=(10, 7), sharex=True, sharey=True
)

max_length = max(result["max_length"] for result in results)

for ax, result in zip(axes.flat, results):
       ax.bar(result["ks"], result["probabilities"])

    ax.set_title(f"Q = {result['Q']}")
    ax.set_xlabel("Continued fraction length k")
    ax.set_ylabel("Probability P_Q(k)")
    ax.set_xticks(range(1, max_length + 1))

fig.suptitle("Distribution of continued fraction lengths")
fig.tight_layout()
plt.show()

# 5. Interpretation
# The mean length increases from approximately 2.63 for Q = 20 to 4.51 for Q = 200. The standard deviation increases from approximately 1.06 to 1.52. The distribution therefore shifts towards longer expansions and becomes more spread out.
# The Fibonacci formula gives the maximum possible length:
# k_max(Q) = max{k : F_{k+2} <= Q}.
#
# The maximum lengths for Q = 20, 50, 100 and 200 are 5, 7, 9 and 10 respectively, agreeing with the formula.
# For example, F_12 = 144 <= 200, but F_13 = 233 > 200.
# Therefore, a fraction with denominator at most 200 can have length 10, but cannot have length 11.
#
# Fibonacci numbers grow approximately exponentially.
# Consequently, the maximum possible length grows logarithmically with Q.
#
# The maximum length is not the most common length. For Q = 200, the most frequent length is 4, with 3018 fractions. Only three fractions have length 10.
# Near the maximum possible length, the coefficients are strongly restricted by the denominator bound: increasing coefficients increases the denominator. This helps explain why very long expansions are rare in these finite distributions.
#
# The sequence d_k determines when a length first becomes possible.
# It does not determine the probability of that length; those probabilities are calculated separately through P_Q(k).

# Comparison with Core 3
#
# For phi = 1, the statistic S_1(x) equals the continued fraction length ell(x).
#
# For Q = 100, the full-set mean length from Core 4 is
# 3.9244, and the standard deviation is 1.3906.
#
# Core 3 uses uniform random sampling with replacement.
# Its sample statistics may differ from the full-set values because of random sampling variation.
