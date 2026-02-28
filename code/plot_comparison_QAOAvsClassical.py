import matplotlib.pyplot as plt
import os

# Data from previous experiments
N = [2, 4, 6, 8]
classical = [1, 4, 9, 16]
qaoa = [1.0,3.0547,4.5742,6.0391]

plt.figure()
plt.plot(N, classical, marker='s', label='Classical Max-Cut')
plt.plot(N, qaoa, marker='o', label='QAOA (Noiseless)')

plt.xlabel("Number of satellites (N)")
plt.ylabel("Max-Cut objective value")
plt.title("QAOA vs Classical Max-Cut Performance")
plt.legend()
plt.grid(True)
plt.tight_layout()

os.makedirs("../figures", exist_ok=True)

plt.savefig("../figures/qaoa_vs_classical.pdf")
plt.show()
