import qutip
from Universal_gates import *

def graph(vec):
	b=qutip.Bloch()
	up=qutip.basis(2,0)
	down=qutip.basis(2,1)
	b.add_states(vec[0]*up+vec[1]*down)
	b.show()

def rotx(theta):
	X = np.zeros([2,2],dtype=complex)
	X[0,0] = X[1,1] = np.cos(theta/2)
	X[0,1] = X[1,0] = -1j*np.sin(theta/2)
	return X
def roty(theta):
	Y = np.zeros([2,2],dtype=complex)
	Y[0,0] = Y[1,1] = np.cos(theta/2)
	Y[0,1] = -1j*np.sin(theta/2)
	Y[1,0] = -Y[0,1]
	return Y

def rotz(theta):
	Z = np.zeros([2,2],dtype=complex)
	Z[0,0] = np.exp(-1j*theta/2)
	Z[1,1] = np.exp(1j*theta/2)
	return Z

def controlU(U, diff, flag):
	C1 = np.zeros((2,2), dtype=complex)
	C2 = np.zeros((2,2), dtype=complex)
	I = np.identity(2)
	Sig = U
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

def onebitUni(U):
	alpha = np.angle(U[0,0]) - np.angle(U[1,0])
	beta = np.angle(U[0,0]) + np.angle(U[1,0])
	theta = np.arctan(np.absolute(U[1,0])/np.absolute(U[0,0]))
	phi = np.angle(np.linalg.det(U))
	A = np.dot(rotz(-alpha),roty(2*theta))
	return np.exp(1j*phi/2)*np.dot(A,rotz(-beta))

def addPhase(valj,jBit,valk,kBit):
	return 1.0*(valj*valk)/2**(jBit+kBit-1)


def U(j,k,numwire):
	phase = 0.0
	if len(j)<numwire:
		for i in range(numwire-len(j)):
			j = [0] + j
	if len(k)<numwire:
		for i in range(numwire-len(k)):
			k = [0] + k
	for jBit in range(numwire):
		for kBit in range(numwire):
			phase = phase+addPhase(j[jBit],jBit,k[kBit],kBit)
	#print phase
	return np.exp(2.0*1j*np.pi*phase)

def xyModN(x,N, numwire):
	U = []
	u=0.0
	if N>2**numwire:
		print "Use more wires!"
		return
	for i in range(2**numwire):
		#fnal = np.zeros(2**numwire)
		f = np.zeros(2**numwire)
		u = int(x)*i % N
		f[u] = 1
		# if len(fnal)<2**numwire:
		# 	for i in range(2**numwire-len(fnal)):
		# 		fnal = [0] + fnal
		U.append(f)
		
	return np.asarray(U).reshape([2**numwire,2**numwire])

#print np.angle(np.linalg.eigvals(xyModN(3,15,4)))/(2*np.pi)
# k = xyModN(3,15,4)
# b= np.linalg.eig(k)
# print b
###############################UNUSED CODE###############################
# S=[]
# for i in range(8):
# 	k= [int(x) for x in bin(i)[2:]]
# 	for l in range(8):
# 		j= [int(l) for l in bin(l)[2:]]
# 		S.append(U(k,j,3))

# out = np.asarray(S).reshape([8,8])
# print out



# vec = [int(a) for a in bin(u)[2:]]
# 		if len(vec)<numwire:
# 			for i in range(numwire-len(vec)):
# 			 vec = [0] + vec
# 		print vec