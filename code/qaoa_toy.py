import numpy as np
import csv
import os
import time
from qiskit import QuantumCircuit
from qiskit_aer import Aer
from scipy.optimize import minimize

# Config
backend = Aer.get_backend("qasm_simulator")
SHOTS = 512

# Logging
def log_result(tag, energy):
    os.makedirs("results", exist_ok=True)
    with open("results/qaoa_results.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            time.strftime("%Y-%m-%d %H:%M:%S"),
            tag,
            energy
        ])
# QAOA circuit (supports depth p)

def qaoa_circuit(params, p):
    qc = QuantumCircuit(2)
    qc.h([0, 1])

    for layer in range(p):
        gamma = params[2 * layer]
        beta = params[2 * layer + 1]
# Cost unitary
        qc.cx(0, 1)
        qc.rz(2 * gamma, 1)
        qc.cx(0, 1)
# Mixer
        qc.rx(2 * beta, 0)
        qc.rx(2 * beta, 1)

    qc.measure_all()
    return qc
# Expectation ⟨Z₀Z₁⟩
def expectation_zz(counts):
    exp = 0.0
    for bitstring, count in counts.items():
        z0 = 1 if bitstring[1] == "0" else -1
        z1 = 1 if bitstring[0] == "0" else -1
        exp += (count / SHOTS) * z0 * z1
    return exp

for p in [1, 2]:
    print(f"\nRunning QAOA with p = {p}")

    def energy(params):
        qc = qaoa_circuit(params, p)
        job = backend.run(qc, shots=SHOTS)
        counts = job.result().get_counts()
        return expectation_zz(counts)

    init = np.random.rand(2 * p)

    res = minimize(
        energy,
        x0=init,
        method="COBYLA",
        options={"maxiter": 25}
    )

    print(f"p = {p}, energy = {res.fun}")

    log_result(f"p{p}_noiseless", res.fun)
