import csv
import matplotlib.pyplot as plt

tags = []
energies = []

with open("results/qaoa_results.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        if len(row) < 4:
            continue

        tag = row[1]
        energy = row[3]

        if tag in ["noiseless", "noisy"]:
            tags.append(f"{tag}_N{row[2]}")
            energies.append(float(energy))

plt.figure(figsize=(6,4))
plt.bar(tags, energies)
plt.ylabel("Max-Cut Value (C)")
plt.xlabel("Experiment")
plt.title("QAOA Performance Comparison")
plt.grid(axis="y")

plt.tight_layout()
plt.savefig("results/qaoa_energy_comparison.pdf")
plt.show()
