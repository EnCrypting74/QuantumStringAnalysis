from qiskit import *
from qiskit.circuit.library import MCXGate
from qiskit.visualization import plot_histogram
from pytket.extensions.quantinuum import QuantinuumBackend
from pytket.extensions.quantinuum import QuantinuumAPIOffline
from azure.quantum import Workspace
from azure.quantum.qiskit import AzureQuantumProvider
from pytket.extensions.qiskit import qiskit_to_tk
import qsharp

mode = 'Simulate' # Run in order Offline -> Syntax -> Simulate -> H1

# Job definition
def palindrome():
        

        x = [1, 1, 0, 0, 1, 1]

        size = len(x)

        # Definire i registri quantistici e classici
        qx = QuantumRegister(size, name='string_x')
        q_results = QuantumRegister(size // 2, name='output')
        qbit = QuantumRegister(1)
        cr = ClassicalRegister(1)

        qc = QuantumCircuit(qx, q_results, qbit, cr)

        # Inizializzare i qubit con i valori di x
        for i in range(size):
                if x[i] == 1:
                        qc.x(qx[i])
        qc.barrier()


        for i in range(size // 2):
                qc.ccx(qx[i], qx[size - 1 - i], q_results[i])  # Use CCX to copy parity check result

        qc.barrier()

        for i in range(size):
                qc.x(qx[i])

        qc.barrier()

        for i in range(size // 2):
                qc.ccx(qx[i], qx[size - 1 - i], q_results[i])  # Use CCX to copy parity check result

        qc.barrier()

        for i in range(size):
                qc.x(qx[i])


        #for i in range(size//2):
        #     qc.x(q_results[i])    
        # Aggiungere la porta MCX
        mcx_gate = MCXGate(size // 2)
        qc.append(mcx_gate, q_results[:] + qbit[:])

        # Misurare il qubit
        qc.measure(qbit[0], cr[0])

        # Visualizzare il circuito
        print(qc.draw())

        return qc

qc = palindrome()

## Common settings
n_shots = 100
# Reset the compiler to target the adequate profile
qsharp.init(target_profile=qsharp.TargetProfile.Adaptive_RI)

if mode == 'Offline':
    # Execute the circuit on a local simulation of the H1 architecture, doesn't cost credits
    api_offline = QuantinuumAPIOffline()
    backend = QuantinuumBackend(device_name = "H1-1LE", api_handler = api_offline)

    qc = qiskit_to_tk(qc)
    compiled_circ = backend.get_compiled_circuit(qc) 
    handle = backend.process_circuit(compiled_circ, n_shots=100)

    result = backend.get_result(handle)
    print(result.get_counts())
    plot_histogram(result.get_counts(qc), title="Result", number_to_keep=2)

    
elif mode == 'Syntax': # teoricamente funziona
        #Syntax Checker for the H1 model, doesn't cost credits or tokens    
    # Select Workspace and Backend 
    
    workspace = Workspace(
            resource_id = "/subscriptions/38b1da4a-afc7-4542-a3a5-4a6e98428e65/resourceGroups/QComputing/providers/Microsoft.Quantum/Workspaces/QuantumStringComparisonResearch",
            location = "westeurope")

    provider = AzureQuantumProvider(workspace)
    backend = provider.get_backend("quantinuum.sim.h1-1sc")
    
    # Using the Quantinuum target, call "run" to submit the job. We'll
    # use 100 shots (simulated runs).
    job = backend.run(qc, shots=n_shots)
    print("Job id:", job.id())
    result = job.result()
    print(result.get_counts(qc))
    plot_histogram(result.get_counts(qc), title="Result", number_to_keep=2)

elif mode == 'Simulate':
        # Simulate on the cloud-hosted H1 simulator, we can select between state_vector or stabilizer sim methods
    
    # Select Workspace and Backend 
    
    workspace = Workspace(
            resource_id = "/subscriptions/38b1da4a-afc7-4542-a3a5-4a6e98428e65/resourceGroups/QComputing/providers/Microsoft.Quantum/Workspaces/QuantumStringComparisonResearch",
            location = "westeurope")

    provider = AzureQuantumProvider(workspace)
    backend = provider.get_backend("quantinuum.sim.h1-1e")
    
    # Using the Quantinuum target, call "run" to submit the job. We'll
    # use 100 shots (simulated runs).
    job = backend.run(qc, shots=n_shots)
    print("Job id:", job.id())
    result = job.result()
    print(result.get_counts(qc))
    
    plot_histogram(result.get_counts(qc), title="Result", number_to_keep=2)
    
    # Calculate the cost of the operation, currently bugs in the qasm2 convertion of the circuit
    #op_cost = backend.estimate_cost(qc, shots = n_shots)
    #print(op_cost)
    
elif mode == 'H1':
        # Execute the circuit on the H1 hardware

    # Select Backend and log into the selected machine# Select Workspace and Backend 
    
    workspace = Workspace(
            resource_id = "/subscriptions/38b1da4a-afc7-4542-a3a5-4a6e98428e65/resourceGroups/QComputing/providers/Microsoft.Quantum/Workspaces/QuantumStringComparisonResearch",
            location = "westeurope")

    provider = AzureQuantumProvider(workspace)
    backend = provider.get_backend("quantinuum.qpu.h1-1")
    
    # Using the Quantinuum target, call "run" to submit the job. We'll
    # use 100 shots (simulated runs).
    job = backend.run(qc, shots=n_shots)
    print("Job id:", job.id())
    result = job.result()
    print(result.get_counts(qc))
    