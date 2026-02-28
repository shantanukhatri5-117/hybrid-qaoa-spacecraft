import csv
import matplotlib.pyplot as plt

depth = []
energy = []

with open("results/qaoa_results.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        
        if row[1].startswith("p") and "noiseless" in row[1]:
            p = int(row[1][1])      # p1 → 1, p2 → 2
            depth.append(p)
            energy.append(float(row[2]))

        
        elif row[1] == "noiseless" and len(row) == 4:
            depth.append(int(row[2]))
            energy.append(float(row[3]))


depth, energy = zip(*sorted(zip(depth, energy)))

plt.plot(depth, energy, marker="o")
plt.xlabel("QAOA Depth p")
plt.ylabel("Energy ⟨H⟩")
plt.title("Effect of QAOA Depth on Performance")
plt.grid(True)
plt.tight_layout()

plt.savefig("results/qaoa_depth_vs_energy.pdf")
plt.show()
