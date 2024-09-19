#Library for Quantum LCS with personalized gate and other stuff


from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import *
import numpy as np
import math
import sys
######################################################################################
#Rotation gate (not controlled) -> rot
def rot(n, k, block_size): # n*block_size vs n, block_size
    qc = QuantumCircuit(n, name=f'rot_k={k}')
    stop = (int(np.log2(n)) - int(np.log2(k*block_size)) + 2)
    #print("stop = ", stop)
    for i in range(block_size, stop):
        #print("\nnumero = ", int(n/(k*(2**i))))
        for j in range(0, int(n/(k*(2**i)))):
            for x in range(j*k*(2**i), k*((j*2**i+1))):
                for offset in range(0, block_size):
                    inizio_swap = x + k*offset
                    fine_swap = x + 2**(i-1)*k + k*offset

                    
                    qc.swap(inizio_swap, fine_swap)
                    print("\n inizio swap = ", inizio_swap)
                    print("\n fine swap = ", fine_swap)
     #               qc.barrier()
                    #qc.swap(inizio_swap + 1, fine_swap + 1)
                    #qc.swap(inizio_swap + 2, fine_swap + 2)
             
    print(qc)  
    #sys.exit()           
    rot_gate = qc.to_gate()
    return rot_gate 


   

def crot(n, k, block_size):
    # Creiamo il gate di rotazione come prima
    rot_gate = rot(n, k, block_size)
    
    # Aggiungiamo un qubit di controllo al gate per renderlo controllato
    c_rot_gate = rot_gate.control(1)
    
    return c_rot_gate
######################################################################################
#Rotation gate (not controlled) -> rot
def rot_qec(n, k, block_size, encoding): # n*block_size vs n, block_size
    qc = QuantumCircuit(n, name=f'rot_k={k}')
    n=n//encoding
    stop = (int(np.log2(n)) - int(np.log2(k*block_size)) + 2)
    #print("stop = ", stop)
    for i in range(block_size, stop):
        #print("\nnumero = ", int(n/(k*(2**i))))
        for j in range(0, int(n/(k*(2**i)))):
            for x in range(j*k*(2**i), k*((j*2**i+1))):
                for offset in range(0, block_size):
                    inizio_swap = x + k*offset
                    fine_swap = x + 2**(i-1)*k + k*offset
                    for b in range(encoding):
                        qc.swap(inizio_swap*encoding + b , fine_swap*encoding + b)
                        print("\n inizio swap = ", inizio_swap)
                        print("\n fine swap = ", fine_swap)


                        #print("\ninizio_swap + b", inizio_swap + b)
                        #print("\nfine_swap + b", fine_swap + b)
                    #qc.swap(inizio_swap + 1, fine_swap + 1)
                    #qc.swap(inizio_swap + 2, fine_swap + 2)
             
    print(qc)             
    rot_gate = qc.to_gate()
    return rot_gate 


   

def crot_qec(n, k, block_size, encoding):
    # Creiamo il gate di rotazione come prima
    rot_gate = rot_qec(n, k, block_size, encoding)
    
    # Aggiungiamo un qubit di controllo al gate per renderlo controllato
    c_rot_gate = rot_gate.control(1)
    
    return c_rot_gate

######################################################################################
#M match operatore to gate -> M_match

def m_match(n_qubits):

    qx = QuantumRegister(n_qubits, 'qx')
    qy = QuantumRegister(n_qubits, 'qy')
    qlam0 = QuantumRegister(n_qubits, 'qlam0')  

    # Crea il circuito quantistico che rappresenta il gate M_match
    qc = QuantumCircuit(qx, qy, qlam0, name='M match')

    #qc.barrier()
    for i in range(n_qubits):
        qc.ccx(qx[i], qy[i], qlam0[i])

    #qc.barrier()    
    for i in range(n_qubits):    
        qc.x(qx[i])
        qc.x(qy[i])

    #qc.barrier()
    for i in range(n_qubits):
        qc.ccx(qx[i], qy[i], qlam0[i])

    #qc.barrier()    
    for i in range(n_qubits):    
        qc.x(qx[i])       
        qc.x(qy[i])    
   
    M_gate = qc.to_gate()
    return M_gate
    #m_gate = qc.to_gate().control(2)
    #return m_gate
############################################
#extended operator 
def ext(order, qr1, qr2):
    qc = QuantumCircuit(qr1, qr2, name=f'ext_{order}')

    for i in range(0, len(qr2), 2):
        if i + order < len(qr1):  
            qc.ccx(qr1[i], qr1[i+order], qr2[i])

    for i in range(1, len(qr2), 2):
        if i + order < len(qr1):  
            qc.ccx(qr1[i], qr1[i+order], qr2[i])
    

    #print(qc)
    # Converti il circuito in un gate personalizzato
    ext_gate = qc.to_gate()
    
    return ext_gate

###################################register reversal operator
#->Inverting register qbits of size n by n/2 parallel swaps
def rro(n):
    qr = QuantumRegister(n, 'qr')
    qc = QuantumCircuit(qr, name='rro')
    for i in range(n // 2):
        qc.swap(qr[i], qr[n - i - 1])
    
    rro_gate = qc.to_gate()
    
    return rro_gate

###################################controlled bitwise conjunction operator
#->Perform a controlled logical AND between two registers only if control qbubits == 0 (reverse control)
def cbco(n_qubits):
    qa = QuantumRegister(n_qubits, 'qa') #qa e qb registri in cui codifico le stringhe
    qb = QuantumRegister(n_qubits + 1, 'qb')
    qr = QuantumRegister(n_qubits + 1, 'qr') #salvo il risultato dell'and
    bco = QuantumCircuit(qa, qb, qr, name='bco')

    for i in range(n_qubits):
        bco.ccx(qa[i], qb[i], qr[i])

    #print(bco)    
    cbco_gate = bco.to_gate().control(1)

    return cbco_gate

###################################copy operator with reversal control
#->Copy a know register of size n_qubits on another register, with a reverse control on a common qubit 
def copy(n_qubits):    
    qa = QuantumRegister(n_qubits + 1, 'qa') #stringa da copiare
    qb = QuantumRegister(n_qubits + 1, 'qb') #target
    #ctrl = QuantumRegister(n_qubits, 'ctrl')
    copy = QuantumCircuit(qa, qb, name='copy')

    for i in range(n_qubits):   
        copy.cx(qa[i], qb[i])

    copy_gate = copy.to_gate().control(1)    
    return copy_gate


###################################register disjunction operator
#->computed logical or between n qubits of input register and deposito the result in a qubit

def disjunction(n_qubits):
    qa = QuantumRegister(n_qubits, 'qa')
    qr = QuantumRegister(1, 'qr')

    disjunction = QuantumCircuit(qa, qr, name='disj')

    disjunction.x(qa[:])
    disjunction.mct(qa[:], qr[0])
    disjunction.x(qa[:])
    disjunction.x(qr[0])

    #print(disjunction)

    disjunction_gate = disjunction.to_gate()
    return disjunction_gate




    
