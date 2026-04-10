import numpy as np
import matplotlib.pyplot as plt

n = np.arange(-10, 10)

x = np.zeros_like(n)

valid_indices = (n == 4)
x[valid_indices] = 2 ** 4

plt.stem(n, x, basefmt="black")

plt.title(r"Discrete Signal $x(n) = 2^n*\delta(n-4)$")
plt.xlabel("n (discrete time)")
plt.ylabel("x(n)")
plt.xticks(n)  # Force ticks at every integer
plt.grid(True, linestyle='--', alpha=0.7)

plt.savefig("plot.png")
