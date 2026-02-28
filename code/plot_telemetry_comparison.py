import matplotlib.pyplot as plt
import os

labels = ["Synthetic Graph", "Telemetry-Grounded Graph"]
energies = [1.9219, 2.4068]  

plt.figure()
plt.bar(labels, energies)
plt.ylabel("Optimized Max-Cut Energy ⟨H⟩")
plt.title("Synthetic vs Telemetry-Grounded QAOA Optimization")

plt.tight_layout()
os.makedirs("../figures", exist_ok=True)
plt.savefig("../figures/telemetry_comparison.pdf")
plt.show()
