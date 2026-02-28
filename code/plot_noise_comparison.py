# plot_noise_comparison.py
# Noiseless vs Noisy comparison (robust)

import csv
import matplotlib.pyplot as plt
from collections import defaultdict

data = defaultdict(dict)

with open("results/qaoa_results.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        if len(row) != 4:
            continue  # skip old-format rows

        _, tag, N, energy = row
        data[int(N)][tag] = float(energy)

Ns = sorted(data.keys())

noiseless = [data[N].get("noiseless") for N in Ns]
noisy = [data[N].get("noisy") for N in Ns]

plt.figure()
plt.plot(Ns, noiseless, marker="o", label="Noiseless")
plt.plot(Ns, noisy, marker="s", label="Noisy")
plt.xlabel("Number of satellites (N)")
plt.ylabel("Energy (MaxCut objective)")
plt.title("Effect of Noise on QAOA Performance")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
