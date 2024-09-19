from qiskit import * 

import lcs  
import math
import res_count
import numpy as np
import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram
from pytket.extensions.quantinuum import QuantinuumBackend
from pytket.extensions.quantinuum.backends.api_wrappers import QuantinuumAPIOffline
from azure.quantum import Workspace
from azure.quantum.qiskit import AzureQuantumProvider
from pytket.extensions.qiskit import qiskit_to_tk

mode = 'Simulate' # Run in order Syntax -> Simulate -> H1
qec = 'no' #yes or no

shots = 1000

encoding = 1
anc = 2
alphabet = ['0', '1']
sigma = len(alphabet)
dim = 2
string = [1] + [0] * (dim-1)
n = len(string)
target_qubits = encoding*n
control_qubits = math.ceil(np.log2(n)) 
ancilla_qubits = anc
ancilla_bits = anc*n
block_size = int(np.log2(sigma))  # Esempio, usando un alfabeto di dimensione 4

control_register = QuantumCircuit(control_qubits, name='control')
target_register = QuantumRegister(target_qubits, name='target')
ancilla_register = QuantumRegister(ancilla_qubits, name='ancilla')
target_indices = list(range(control_qubits, target_qubits + control_qubits))
control_indices = list(range(control_qubits))




ancilla = QuantumCircuit(anc)
# Crea un circuito combinato con una dimensione totale di n + log2(n) qubit
qc = QuantumCircuit(control_qubits)
qc.add_register(target_register)
qc.add_register(ancilla_register)

classical_registers = []
for i in range(n):
    classical_reg = ClassicalRegister(anc, f'classical_ancilla_{i}')
    qc.add_register(classical_reg)
    classical_registers.append(classical_reg)


#sovrapposizione dei qbit di controllo
for j in range(control_qubits):
	qc.h(j)



#codifico la stringa nei qbit target
temp = 0
for i in range(n):
	if string[i] == 1:
		for j in range(encoding):
			qc.x(target_register[temp+j])
	temp += encoding		


qc.barrier()
control_indices = 0
for c_qbits in range(0, control_qubits):
	k = 2**c_qbits
	my_crot_gate = lcs.crot_qec(target_qubits, k, block_size, encoding)
	qc.append(my_crot_gate, [c_qbits] + target_indices)


###############QEC#####################################################

if qec == 'yes':
    qc.barrier()
    for i, j, f in zip(range(0, target_qubits, encoding), range(0, ancilla_bits, anc), range(n)):
        print("i=", i)
        print("j=", j)
        qc.cx(target_register[i], ancilla_register[0])
        qc.cx(target_register[i+1], ancilla_register[0])
        qc.cx(target_register[i+1], ancilla_register[1])
        qc.cx(target_register[i+2], ancilla_register[1])
        qc.barrier()
        qc.measure(ancilla_register[0], classical_registers[f][0])
        qc.measure(ancilla_register[1], classical_registers[f][1])
        qc.barrier()
        qc.reset(ancilla_register[0])
        qc.reset(ancilla_register[1])
        qc.barrier()
        qc.x(target_register[i+2]).c_if(classical_registers[f], 2)  # Applica X sul terzo qubit se il risultato è 01
        qc.x(target_register[i]).c_if(classical_registers[f], 1)    # Applica X sul primo qubit se il risultato è 10
        qc.x(target_register[i+1]).c_if(classical_registers[f], 3)  # Applica X sul secondo qubit se il risultato è 11
        qc.barrier()



###############misura##################################################
qc.barrier()
classic_register = ClassicalRegister(target_qubits, name='target_classic')
qc.add_register(classic_register)

qc.measure(target_register, classic_register)

depth = qc.depth()
print("\ndepth = ", depth)
print(qc.draw())

###############simulazione##################################################
if mode == 'Syntax':	
   
    workspace = Workspace(
            resource_id = "/subscriptions/38b1da4a-afc7-4542-a3a5-4a6e98428e65/resourceGroups/QComputing/providers/Microsoft.Quantum/Workspaces/QuantumStringComparisonResearch",
            location = "westeurope")

    provider = AzureQuantumProvider(workspace)
    backend = provider.get_backend("quantinuum.sim.h1-1sc")
    
    # Using the Quantinuum target, call "run" to submit the job. We'll
    # use 100 shots (simulated runs).
    job = backend.run(qc, shots= shots)
    print("Job id:", job.id())
    result = job.result()
    print(result.get_counts(qc))
    plot_histogram(result.get_counts(qc), title="Result", number_to_keep=2)
    

    print(qc)	
	#plt.show()

elif mode=='H1': # Run circuit on the Quantinuum h1 processor
 # Select Backend and log into the selected machine# Select Workspace and Backend 
    
    workspace = Workspace(
            resource_id = "/subscriptions/38b1da4a-afc7-4542-a3a5-4a6e98428e65/resourceGroups/QComputing/providers/Microsoft.Quantum/Workspaces/QuantumStringComparisonResearch",
            location = "westeurope")

    provider = AzureQuantumProvider(workspace)
    backend = provider.get_backend("quantinuum.qpu.h1-1")
    
    transpiled_circuit = transpile(qc, backend, optimization_level=3)
    job = backend.run(transpiled_circuit, shots = 1024)
    result = job.result()
    counts = result.get_counts()
    plot_histogram(counts)

elif mode == 'Simulate':
        # Simulate on the cloud-hosted H1 simulator, we can select between state_vector or stabilizer sim methods
    
    # Select Workspace and Backend 
    
    workspace = Workspace(
            resource_id = "/subscriptions/38b1da4a-afc7-4542-a3a5-4a6e98428e65/resourceGroups/QComputing/providers/Microsoft.Quantum/Workspaces/QuantumStringComparisonResearch",
            location = "westeurope")

    provider = AzureQuantumProvider(workspace)
    backend = provider.get_backend("quantinuum.sim.h1-1e")
    
    # Using the Quantinuum target, call "run" to submit the job. We'll
    # use 1000 shots (simulated runs).
    job = backend.run(qc, shots=shots)
    print("Job id:", job.id())
    result = job.result()
    print(result.get_counts(qc))
    res_count.res(result.get_counts(qc))
    
    plot_histogram(result.get_counts(qc), title="Result", number_to_keep=2)
    
    # Calculate the cost of the operation, currently bugs in the qasm2 convertion of the circuit
    #op_cost = backend.estimate_cost(qc, shots = n_shots)
    #print(op_cost)