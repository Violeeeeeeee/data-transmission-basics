import numpy as np
import matplotlib.pyplot as plt

# Define the discrete time vector 'n' (e.g., from -2 to 10)
n = np.arange(-2, 11)

# Initialize the signal array 'x' with zeros
x = np.zeros_like(n)

# The delta function only "fires" when n = 3k (which means n >= 0 and n is a multiple of 3)
# So, we find all indices where n >= 0 AND n % 3 == 0
valid_indices = (n >= 0) & (n % 3 == 0)
# For those valid points, k = n / 3. The amplitude is (-1)^k
k = n[valid_indices] // 3
x[valid_indices] = (-1.0) ** k

# Plot the discrete signal using plt.stem()
# basefmt="black" makes the horizontal axis line black
plt.stem(n, x, basefmt="black")

# Formatting the plot to make it look like a proper textbook sketch
plt.title(r"Discrete Signal $x(n) = \sum (-1)^k \delta(n-3k)$")
plt.xlabel("n (discrete time)")
plt.ylabel("x(n)")
plt.xticks(n)  # Force ticks at every integer
plt.grid(True, linestyle='--', alpha=0.7)

plt.savefig("plot.png")
