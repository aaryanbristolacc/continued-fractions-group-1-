#For a reduced fraction \(x=a/q\) in \((0,1)\), we use its canonical
#continued fraction expansion
\[
x=[0;a_1,\ldots,a_k],
\]
#where the final coefficient satisfies \(a_k\geq2\).

#The length is \(\ell(x)=k\). The initial coefficient \(a_0=0\) is not counted. We calculate the coefficients using the Euclidean algorithm with integer arithmetic. This avoids rounding errors
from repeated calculations with floating-point numbers.
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

Let \(d_k\) be the smallest denominator of a rational number in \((0,1)\) with continued fraction length \(k\).

The convergent denominators satisfy
\[
q_{-1}=0,\qquad q_0=1,\qquad
q_j=a_jq_{j-1}+q_{j-2}.
\]

For a canonical expansion of length \(k\), the coefficients satisfy \(a_j\geq1\) for \(1\leq j<k\), and \(a_k\geq2\).
The recurrence is increasing in each coefficient, so the smallest denominator is obtained by choosing
\[
a_1=\cdots=a_{k-1}=1,\qquad a_k=2.
\]

For \(k=1\), the smallest fraction is \([0;2]=1/2\), so \(d_1=2\).
For \(k\geq2\), the coefficients before the final term give
\(q_j=F_{j+1}\). Therefore,
\[
d_k=2F_k+F_{k-1}=F_{k+2},
\]
where \(F_0=0\) and \(F_1=1\).

Thus,
\[
\boxed{d_k=F_{k+2}},
\]
giving the sequence \(2,3,5,8,13,21,\ldots\).

A fraction attaining this minimum is
\[
\frac{F_{k+1}}{F_{k+2}}
=
[0;\underbrace{1,\ldots,1}_{k-1\text{ terms}},2].
\]

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

## Distribution of continued fraction lengths

For each denominator bound \(Q\), we enumerate every fraction
in \(\mathcal F_Q\) once. We calculate
\[
c_Q(k)=\#\{x\in\mathcal F_Q:\ell(x)=k\},
\qquad
P_Q(k)=\frac{c_Q(k)}{\#\mathcal F_Q}.
\]

Since we use the full set, these probabilities are exact for the chosen values of \(Q\), rather than estimates from a random sample.
We use moderate values of \(Q\) because full enumeration becomes expensive as \(Q\) increases.

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

    # Largest length permitted by the minimum-denominator formula.
    predicted_max = 0
    while core4_fibonacci(predicted_max + 3) <= Q:
        predicted_max += 1

    assert np.isclose(probabilities.sum(), 1.0)
    assert int(ks[-1]) == predicted_max

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

# Length distributions
fig, axes = plt.subplots(
    2, 2, figsize=(10, 7), sharex=True, sharey=True
)

max_length = max(result["max_length"] for result in results)

for ax, result in zip(axes.flat, results):
    ax.bar(
        result["ks"],
        result["probabilities"],
        width=0.8,
        edgecolor="black"
    )

    ax.set_title(f"Q = {result['Q']}")
    ax.set_xlabel("Continued fraction length k")
    ax.set_ylabel("Probability P_Q(k)")
    ax.set_xticks(range(1, max_length + 1))

plt.tight_layout()
plt.show()

# Report c_Q(k) and P_Q(k) for the largest Q.
last = results[-1]

print(f"\nDetailed distribution for Q = {last['Q']}")
print(" k | c_Q(k) | P_Q(k)")

for k, count, probability in zip(
    last["ks"], last["counts"], last["probabilities"]
):
    print(f"{k:2d} | {count:6d} | {probability:.6f}")

## Interpretation
The Fibonacci formula determines the largest possible length:
\[
k_{\max}(Q)=\max\{k:F_{k+2}\leq Q\}.
\]

For example, when \(Q=200\), we have \(F_{12}=144\leq200\) but
\(F_{13}=233>200\). Therefore, the largest possible length is 10.

The minimum denominator grows approximately exponentially with the length. Consequently, the maximum possible length grows logarithmically with \(Q\).

The formula describes which lengths are possible. It does not, by itself, determine how frequently each length occurs. The frequencies are calculated separately through \(P_Q(k)\).

fig, ax = plt.subplots(figsize=(8, 5))

# Common bins for all standardised distributions.
bins = np.linspace(-5, 5, 41)

for result in results:
    z = (
        (result["ks"] - result["mean"])
        / result["sd"]
    )

    # Weighted histogram: each length receives its exact probability.
    ax.hist(
        z,
        bins=bins,
        weights=result["probabilities"],
        density=True,
        histtype="step",
        linewidth=1.5,
        label=f"Q = {result['Q']}"
    )

ax.set_xlabel("Standardised continued fraction length")
ax.set_ylabel("Density")
ax.legend()

plt.tight_layout()
plt.show()

