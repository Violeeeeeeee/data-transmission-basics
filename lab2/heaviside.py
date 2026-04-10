import numpy as np
import matplotlib.pyplot as plt

# Definiujemy wektor n (np. od -10 do 3, żeby dobrze było widać zjawisko)
n = np.arange(-10, 4)

# Inicjalizujemy tablicę sygnału samymi zerami (float, żeby obsłużyć -1.0 i 1.0)
x = np.zeros_like(n, dtype=float)

# MASKOWANIE LOGICZNE (Poprawny sposób w NumPy zamiast 'if')
# Znajdujemy indeksy, dla których n <= -4 (czyli tam, gdzie u(-n-4) wynosi 1)
valid_indices = n <= -4

# 4. Obliczamy wartości TYLKO dla tych miejsc, w których funkcja "żyje"
x[valid_indices] = (-1.0) ** n[valid_indices]

plt.figure(figsize=(8, 4))
plt.stem(n, x, basefmt="black")

plt.title(r"Discrete signal $x(n) = (-1)^n u(-n-4)$")
plt.xlabel("n (time)")
plt.ylabel("x(n)")
plt.xticks(n)
plt.grid(True, linestyle='--', alpha=0.7)

plt.savefig("plot_b.png")
plt.show()
