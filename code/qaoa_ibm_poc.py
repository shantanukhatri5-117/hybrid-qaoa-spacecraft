import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import Aer
from scipy.optimize import minimize

backend = Aer.get_backend("qasm_simulator")
SHOTS = 512

# 2-qubit MaxCut: H = Z0 Z1

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


def expectation_zz(counts):
    exp = 0.0
    for bitstring, count in counts.items():
        z0 = 1 if bitstring[1] == "0" else -1
        z1 = 1 if bitstring[0] == "0" else -1
        exp += (count / SHOTS) * z0 * z1
    return exp


def energy(params):
    gamma, beta = params
    qc = qaoa_circuit(gamma, beta)

    job = backend.run(qc, shots=SHOTS)
    result = job.result()
    counts = result.get_counts()

    return expectation_zz(counts)


# Classical optimization loop
res = minimize(
    energy,
    x0=[0.5, 0.5],
    method="COBYLA",
    options={"maxiter": 20}
)

print("Optimal (gamma, beta):", res.x)
print("Minimum energy:", res.fun)

