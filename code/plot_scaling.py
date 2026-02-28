# plot_scaling.py
# Energy vs number of satellites (noiseless, robust)

import csv
import matplotlib.pyplot as plt

Ns = []
energies = []

with open("results/qaoa_results.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        if len(row) != 4:
            continue  # skip old-format rows

        _, tag, N, energy = row
        if tag == "noiseless":
            Ns.append(int(N))
            energies.append(float(energy))

Ns, energies = zip(*sorted(zip(Ns, energies)))

plt.figure()
plt.plot(Ns, energies, marker="o")
plt.xlabel("Number of satellites (N)")
plt.ylabel("Energy (MaxCut objective)")
plt.title("QAOA Scaling Under Noiseless Simulation")
plt.grid(True)
plt.tight_layout()
plt.show()
