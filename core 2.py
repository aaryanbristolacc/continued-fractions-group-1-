# This function calculates each convergent in order adding another term of the continued fraction at a time
def convergents(cf):

    # These are the starting values
    p_minus2 = 1
    p_minus1 = cf[0]

    q_minus2 = 0
    q_minus1 = 1

    fractions = []

    fractions.append((p_minus1, q_minus1))

    # Creating a loop to calculate the next convergents
    for k in range(1, len(cf)):

        p = cf[k] * p_minus1 + p_minus2
        q = cf[k] * q_minus1 + q_minus2

        # Storing new fraction
        fractions.append((p, q))
        
        # Updating the values
        p_minus2 = p_minus1
        p_minus1 = p

        q_minus2 = q_minus1
        q_minus1 = q

    return fractions

# The next part is checking the error bound
# Calculate the continued fraction expansion of root 5, up to depth 10.
cf = continued_fraction(math.sqrt(5), 10)

results = convergents(cf)

theta = math.sqrt(5)

for fraction in results:

    p = fraction[0]
    q = fraction[1]

    # Error calculates the actual difference between root 5 and tghe convergent
    # Bound calculates the maximum error allowed
    error = abs(theta - p/q)
    bound = 1/(q*q)

    print("Fraction:", p, "/", q)
    print("Error:", error)
    print("Bound:", bound)
    print("Bound satisfied:", error < bound)
    print()

# The results show that the error was smaller than the bound for each convergent tested.
# This provides evidence that support the inequality

# The point of this is to find the best fraction that gives the most accurate value closest to the exact result
def closest_fraction(theta, N):

    cf = continued_fraction(theta, 20)

    fractions = convergents(cf)

    best_fraction = None
    smallest_error = float("inf")

    # Check the convergents
    for fraction in fractions:

        p = fraction[0]
        q = fraction[1]

        if q <= N:

            error = abs(theta - p/q)

            if error < smallest_error:
                smallest_error = error
                best_fraction = (p, q)

    # Check the semiconvergents
    for k in range(2, len(cf)):

        for t in range(1, cf[k] + 1):

            p = fractions[k-2][0] + t * fractions[k-1][0]
            q = fractions[k-2][1] + t * fractions[k-1][1]

            if q <= N:

                error = abs(theta - p/q)

                if error < smallest_error:
                    smallest_error = error
                    best_fraction = (p, q)
    
    
    return Fraction(best_fraction[0], best_fraction[1])

# Test
print("The closest fraction is:", closest_fraction(math.sqrt(5), 10))

# Now applying to e, pi and phi
# Recalling from maths Libary
pi = math.pi
e = math.e
phi = (1 + math.sqrt(5)) / 2

# Find the closest fractions of them
# I tested a few different maximum deominators as it affects how accurate the fraction is to the exact value
print("Pi:", closest_fraction(pi, 150))
print("e:", closest_fraction(e, 100))
print("Golden ratio:", closest_fraction(phi, 100))

import matplotlib.pyplot as plt
import numpy as np

# Store the numbers and their names
numbers = [pi, e, phi]
names = ["Pi", "e", "Golden ratio"]

# Plot each number
for i in range(3):

    theta = numbers[i]
    name = names[i]

    cf = continued_fraction(theta, 20)
    fractions = convergents(cf)

    log_q = []
    log_error = []

    # Calculate the logarithms
    for fraction in fractions:

        p = fraction[0]
        q = fraction[1]

        error = abs(theta - p/q)

        if error > 0:
            log_q.append(np.log(q))
            log_error.append(np.log(error))

    plt.plot(log_q, log_error, marker="o", label=name)

# Add labels and title
plt.xlabel("log(q)")
plt.ylabel("log(|theta - p/q|)")
plt.title("Approximation errors of continued fraction convergents")

plt.legend()
plt.show()


# For Pi: 355/113 this is a very accurate value of pi and it shows continued fractions are very good at finding rational approximations
# With relatively low denominators.

# The graph shows how the accuracy of the fractions changes with larger denominators
# We took logarthims so it is easy to read as error increases
# It gives a linear graph so its we can understand the relationship between the denominators (q) and the error.
# The graph is moving down to the right this is showing:
# The accuracy is getting better, the error is getting smaller, this is happening as the denominators increase.
