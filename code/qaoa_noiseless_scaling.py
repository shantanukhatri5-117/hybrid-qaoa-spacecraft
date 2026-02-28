# qaoa_noiseless_scaling.py
# Noiseless QAOA scaling: 2–8 satellites (p = 1)

import numpy as np
import csv
import os
import time
import networkx as nx
from scipy.optimize import minimize
from qiskit import QuantumCircuit
from qiskit_aer import Aer

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
# QAOA building blocks
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
# MaxCut expectation
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
# Run scaling experiment
# -------------------------
for N in [2, 4, 6, 8]:
    print(f"\nRunning noiseless QAOA for N = {N}")

    G = nx.cycle_graph(N)
    edges = list(G.edges())

    def energy(params):
        qc = qaoa_circuit(params, N, edges)
        job = backend.run(qc, shots=SHOTS)
        counts = job.result().get_counts()
        return -expectation_maxcut(counts, edges)

    res = minimize(
        energy,
        x0=[0.5, 0.5],
        method="COBYLA",
        options={"maxiter": 30}
    )

    maxcut_value = -res.fun
    print(f"N = {N}, maxcut = {maxcut_value}")
    log_result("noiseless", N, maxcut_value)
