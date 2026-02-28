import csv
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import Aer
from scipy.optimize import minimize

def load_telemetry_edges(path):
    edges = []
    with open(path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            i = int(row["i"])
            j = int(row["j"])
            w = float(row["weight"])
            edges.append((i, j, w))
    return edges

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "telemetry_weights.csv")

edges = load_telemetry_edges(DATA_PATH)

NUM_QUBITS = 4

backend = Aer.get_backend("qasm_simulator")
SHOTS = 512

def qaoa_circuit(gamma, beta, edges):
    qc = QuantumCircuit(NUM_QUBITS)
    qc.h(range(NUM_QUBITS))

    # Cost Hamiltonian (weighted ZZ terms)
    for i, j, w in edges:
        qc.cx(i, j)
        qc.rz(2 * gamma * w, j)
        qc.cx(i, j)

    # Mixer
    for q in range(NUM_QUBITS):
        qc.rx(2 * beta, q)

    qc.measure_all()
    return qc

def weighted_expectation(counts, edges):
    energy = 0.0
    for bitstring, count in counts.items():
        prob = count / SHOTS
        for i, j, w in edges:
            zi = 1 if bitstring[::-1][i] == "0" else -1
            zj = 1 if bitstring[::-1][j] == "0" else -1
            energy += prob * w * (1 - zi * zj) / 2
    return energy

def energy_fn(params):
    gamma, beta = params
    qc = qaoa_circuit(gamma, beta, edges)
    job = backend.run(qc, shots=SHOTS)
    counts = job.result().get_counts()
    return -weighted_expectation(counts, edges)

init = np.random.rand(2)
res = minimize(
    energy_fn,
    x0=init,
    method="COBYLA",
    options={"maxiter": 25}
)

print("Telemetry-grounded QAOA")
print("Optimal parameters:", res.x)
print("Optimized energy:", -res.fun)
