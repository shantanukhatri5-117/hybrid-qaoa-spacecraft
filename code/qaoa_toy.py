
from qiskit_aer import Aer
from qiskit.utils import algorithm_globals
from qiskit.circuit.library import QAOAAnsatz
from qiskit.algorithms import QAOA as QiskitQAOA
from qiskit_optimization.applications.ising.max_cut import Maxcut
from qiskit_optimization.converters import QuadraticProgramToQubo
from qiskit_optimization.algorithms import MinimumEigenOptimizer

algorithm_globals.random_seed = 42

graph = {0: [1, 2], 1: [0, 2], 2: [0, 1]}

maxcut = Maxcut(graph)
qp = maxcut.to_quadratic_program()
qp2qubo = QuadraticProgramToQubo()
qubo = qp2qubo.convert(qp)

backend = Aer.get_backend("statevector_simulator")

ansatz = QAOAAnsatz(num_qubits=3, reps=1)
qaoa_alg = QiskitQAOA(ansatz=ansatz, quantum_instance=backend)

meo = MinimumEigenOptimizer(qaoa_alg)
result = meo.solve(qubo)

print("Optimal bitstring:", result.x)
print("Optimal objective:", result.fval)

