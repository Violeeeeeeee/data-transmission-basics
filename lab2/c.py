import numpy as np
import matplotlib.pyplot as plt

n = np.arange(-10, 10)
x = np.zeros_like(n, dtype=float)

valid_indices = (n <= -5) & (n >= -3)

x[valid_indices] = np.cos(np.pi / 2 * n[valid_indices])

plt.figure(figsize=(8, 4))
plt.stem(n, x, basefmt="black")

plt.title(r"Discrete signal $x(n) = \cos(\frac{\pi}{2}n) u(n+3) u(-n-5)$")
plt.xlabel("n (discrete time)")
plt.ylabel("x(n)")
plt.xticks(n)
plt.grid(True, linestyle='--', alpha=0.7)

plt.savefig("plot_c.png")
plt.show()
