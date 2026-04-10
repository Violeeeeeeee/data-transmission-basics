import numpy as np
import matplotlib.pyplot as plt

n = np.arange(-10, 10)

x = np.zeros_like(n)

valid_indices = (n>=0) & ((n-1)%3==0)
k = n[valid_indices]//3
x[valid_indices] = 4

plt.stem(n, x, basefmt="black")

plt.title(r"Discrete Signal $x(n) = \sum 4*\delta(n-3k-1)$")
plt.xlabel("n (discrete time)")
plt.ylabel("x(n)")
plt.xticks(n)  # Force ticks at every integer
plt.grid(True, linestyle='--', alpha=0.7)

plt.savefig("plot.png")

