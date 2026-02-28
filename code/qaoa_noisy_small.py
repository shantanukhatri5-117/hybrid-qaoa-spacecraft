# qaoa_noisy_small.py
# Noisy QAOA (2–4 satellites only)

import numpy as np
import csv
import os
import time
import networkx as nx
from scipy.optimize import minimize
from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit_aer.noise import NoiseModel, depolarizing_error

# -------------------------
# Config
# -------------------------
SHOTS = 512
backend = Aer.get_backend("qasm_simulator")

# -------------------------
# Logging
# -------------------------
def log_result(tag, n, energy):
    os.makedirs("results", exist_ok=True)
    with open("results/qaoa_results.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            time.strftime("%Y-%m-%d %H:%M:%S"),
            tag,
            n,
            energy
        ])

# -------------------------
# Noise model
# -------------------------
noise_model = NoiseModel()
noise_model.add_all_qubit_quantum_error(
    depolarizing_error(0.01, 1), ["rx", "rz"]
)
noise_model.add_all_qubit_quantum_error(
    depolarizing_error(0.02, 2), ["cx"]
)

# -------------------------
# QAOA blocks
# -------------------------
def apply_cost_layer(qc, gamma, edges):
    for (i, j) in edges:
        qc.cx(i, j)
        qc.rz(2 * gamma, j)
        qc.cx(i, j)

def apply_mixer(qc, beta, n):
    for i in range(n):
        qc.rx(2 * beta, i)

def qaoa_circuit(params, n, edges):
    gamma, beta = params
    qc = QuantumCircuit(n)
    qc.h(range(n))
    apply_cost_layer(qc, gamma, edges)
    apply_mixer(qc, beta, n)
    qc.measure_all()
    return qc

# -------------------------
# Expectation
# -------------------------
def expectation_maxcut(counts, edges):
    exp = 0.0
    for bitstring, count in counts.items():
        z = [1 if b == "0" else -1 for b in bitstring[::-1]]
        cost = 0
        for (i, j) in edges:
            cost += (1 - z[i] * z[j]) / 2
        exp += (count / SHOTS) * cost
    return exp

# -------------------------
# Run noisy experiment
# -------------------------
for N in [2, 4]:
    print(f"\nRunning noisy QAOA for N = {N}")

    G = nx.cycle_graph(N)
    edges = list(G.edges())

    def energy(params):
        qc = qaoa_circuit(params, N, edges)
        job = backend.run(
            qc,
            shots=SHOTS,
            noise_model=noise_model
        )
        counts = job.result().get_counts()
        return -expectation_maxcut(counts, edges)

    res = minimize(
        energy,
        x0=[0.5, 0.5],
        method="COBYLA",
        options={"maxiter": 20}
    )

    maxcut_value = -res.fun
    log_result("noisy", N, maxcut_value)

