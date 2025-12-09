from qiskit import Aer, execute
from qiskit.circuit.library import QAOAAnsatz
from qiskit_optimization.applications.ising.max_cut import Maxcut
from qiskit_optimization.converters import QuadraticProgramToQubo
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit.algorithms.minimum_eigensolvers import QAOA
from qiskit.utils import algorithm_globals

algorithm_globals.random_seed = 42

graph = {
    0: [1, 2],
    1: [0, 2],
    2: [0, 1]
}

maxcut = Maxcut(graph)
qp = maxcut.to_quadratic_program()

qp2qubo = QuadraticProgramToQubo()
qubo = qp2qubo.convert(qp)

backend = Aer.get_backend("aer_simulator_statevector")

qaoa = QAOAAnsatz(3, reps=1)
optimizer = QAOA(qaoa=qaoa, optimizer=None)

meo = MinimumEigenOptimizer(optimizer)
result = meo.solve(qubo)

print("Optimal bitstring:", result.x)
print("Optimal objective:", result.fval)

