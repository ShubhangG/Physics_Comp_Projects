import numpy as np
np.set_printoptions(suppress=True, linewidth=np.nan, threshold=np.nan)

def Hadamard():
	H = np.ones((2,2),dtype=complex)
	H[1,1] = -1
	H = H*(1.0/np.sqrt(2))
	return H

def phase(theta):
	Ph = np.identity(2,dtype=complex)
	Ph[1,1] = np.exp(1j*theta)
	return Ph

def Cnot():
	CH = np.identity(4)
	CH[2,2]=CH[3,3]=0
	CH[2,3]=CH[3,2]=1
	return CH

def Cmake(diff, flag):
	C1 = np.zeros((2,2), dtype=complex)
	C2 = np.zeros((2,2), dtype=complex)
	I = np.identity(2)
	Sig = np.zeros((2,2))

	Sig[0,1]=Sig[1,0]=1
	C1[0,0] = 1
	C2[1,1] = 1
	for i in range(diff):
		if flag:
			C1 = np.kron(C1,I)
			C2 = np.kron(C2,Sig)
		else:
			C1 = np.kron(I,C1)
			C2 = np.kron(Sig,C2)

	return C1+C2

def PauliX():
	return np.sqrt(2)*Hadamard() - phase(np.pi)

def PauliZ():
	return phase(np.pi)

def PauliY():
	A =  np.dot(phase(np.pi/2),PauliX())
	return np.dot(A,phase(-np.pi/2))

def CPmake(theta,diff,flag):
	C1 = np.zeros((2,2), dtype=complex)
	C2 = np.zeros((2,2), dtype=complex)
	I = np.identity(2)
	Sig = phase(theta)
	C1[0,0] = 1
	C2[1,1] = 1
	for i in range(diff):
		if flag:
			C1 = np.kron(C1,I)
			C2 = np.kron(C2,Sig)
		else:
			C1 = np.kron(I,C1)
			C2 = np.kron(Sig,C2)

	return C1+C2

