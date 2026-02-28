
# qaoa_noisy.py
# Noisy QAOA experiment (simulator only)

import numpy as np
import csv
import os
import time
from scipy.optimize import minimize

from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit_aer.noise import NoiseModel, depolarizing_error

# Configuring
SHOTS = 512
backend = Aer.get_backend("qasm_simulator")
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
# Noise model (NISQ-like)
noise_model = NoiseModel()
noise_model.add_all_qubit_quantum_error(
    depolarizing_error(0.01, 1), ["rx", "rz"]
)
noise_model.add_all_qubit_quantum_error(
    depolarizing_error(0.02, 2), ["cx"]
)
# QAOA circuit (p = 1)
def qaoa_circuit(gamma, beta):
    qc = QuantumCircuit(2)
    qc.h([0, 1])

    qc.cx(0, 1)
    qc.rz(2 * gamma, 1)
    qc.cx(0, 1)

    qc.rx(2 * beta, 0)
    qc.rx(2 * beta, 1)

    qc.measure_all()
    return qc
#Expectation ⟨Z₀Z₁⟩
def expectation_zz(counts):
    exp = 0.0
    for bitstring, count in counts.items():
        z0 = 1 if bitstring[1] == "0" else -1
        z1 = 1 if bitstring[0] == "0" else -1
        exp += (count / SHOTS) * z0 * z1
    return exp
# Energy function (with noise)
def energy(params):
    gamma, beta = params
    qc = qaoa_circuit(gamma, beta)

    job = backend.run(
        qc,
        shots=SHOTS,
        noise_model=noise_model
    )

    counts = job.result().get_counts()
    return expectation_zz(counts)

print("Running noisy QAOA (p = 1)")

res = minimize(
    energy,
    x0=[0.5, 0.5],
    method="COBYLA",
    options={"maxiter": 20}
)

print("Noisy QAOA energy:", res.fun)

log_result("p1_noisy", res.fun)
