from qiskit_aer import Aer
from qiskit_optimization.applications.ising.max_cut import Maxcut
from qiskit_optimization.converters import QuadraticProgramToQubo
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit.algorithms.minimum_eigensolvers import QAOA
from qiskit.circuit.library import QAOAAnsatz
from qiskit.utils import algorithm_globals

# Seed for reproducibility
algorithm_globals.random_seed = 42

# Define a simple 3-node graph
graph = {
    0: [1, 2],
    1: [0, 2],
    2: [0, 1]
}

# Build MAX-CUT problem
maxcut = Maxcut(graph)
qp = maxcut.to_quadratic_program()

# Convert to QUBO
qp2qubo = QuadraticProgramToQubo()
qubo = qp2qubo.convert(qp)

# Use Aer statevector backend
backend = Aer.get_backend("statevector_simulator")

# QAOA ansatz
qaoa = QAOA(ansatz=QAOAAnsatz(num_qubits=3, reps=1), optimizer=None, quantum_instance=backend)

# Solve
meo = MinimumEigenOptimizer(qaoa)
result = meo.solve(qubo)

print("Optimal bitstring:", result.x)
print("Optimal objective:", result.fval)

