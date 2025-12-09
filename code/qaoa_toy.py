from qiskit import Aer, execute
from qiskit.circuit.library import QAOAAnsatz
from qiskit_optimization.applications.ising.max_cut import Maxcut
from qiskit_optimization.converters import QuadraticProgramToQubo
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit.algorithms.minimum_eigensolvers import QAOA
from qiskit.utils import algorithm_globals

# Set seed
algorithm_globals.random_seed = 42

# Define toy graph (3 nodes)
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

# Simulator backend
backend = Aer.get_backend("aer_simulator_statevector")

# QAOA with depth p=1
qaoa = QAOAAnsatz(3, reps=1)
optimizer = QAOA(qaoa=qaoa, optimizer=None)

# Solve
meo = MinimumEigenOptimizer(optimizer)
result = meo.solve(qubo)

print("Optimal bitstring:", result.x)
print("Optimal objective:", result.fval)

