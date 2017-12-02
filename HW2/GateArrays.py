from Universal_gates import *
from Special_gates import *

def HadamardArray(i,k,undof=0):
	I = np.eye(2)
	H = Hadamard()
	if k==1:
		return H
	Hmat = 1
	for l in range(k):
		if l==i:
			Hmat=np.kron(Hmat,H)
		else:
			Hmat=np.kron(Hmat,I)
	if undof:
		return np.linalg.inv(Hmat)

	return Hmat

def PXArray(i,k):
	I = np.eye(2)
	H = PauliX()
	if k==1:
		return H
	PXmat = 1
	for l in range(k):
		if l==i:
			PXmat=np.kron(PXmat,H)
		else:
			PXmat=np.kron(PXmat,I)
	# if undof:
	# 	return np.linalg.inv(Hmat)

	return PXmat

def PhaseArray(theta,i,k,undof=0):
	I = np.eye(2, dtype=complex)
	P = phase(theta)
	Pmat = 1
	for l in range(k):
		if l==i:
			Pmat=np.kron(Pmat,P)
		else:
			Pmat=np.kron(Pmat,I)
	if undof:
		return np.linalg.inv(Pmat)
	return Pmat


def CNOTArray(cWire, oWire,totalwires,undof=0):
	I = np.eye(2)
	diff = np.abs(cWire-oWire)
	if cWire<oWire:
		CH = Cmake(diff,1)
	else:
		CH = Cmake(diff,0)
	CN = 1
	l=0
	while l < totalwires:
		if l==cWire or l==oWire:
			CN=np.kron(CN,CH)
			if cWire>oWire:
				l=cWire+1
			else:
				l=oWire+1
			continue
		l+=1
		CN= np.kron(CN,I)	
	
	if undof:
		return np.linalg.inv(CN)
	return CN

def CPhaseArray(cWire, oWire, theta, totalwires):
	I = np.eye(2)
	diff = np.abs(cWire-oWire)
	if cWire<oWire:
		CH = CPmake(theta,diff,1)
	else:
		CH = CPmake(theta,diff,0)
	CN = 1
	l=0
	while l < totalwires:
		if l==cWire or l==oWire:
			CN=np.kron(CN,CH)
			if cWire>oWire:
				l=cWire+1
			else:
				l=oWire+1
			continue
		l+=1
		CN= np.kron(CN,I)	

	return CN

def CUArray(U,cWire, oWire, totalwires):
	I = np.eye(2)
	diff = np.abs(cWire-oWire)
	CH = np.copy(U)
	CN = 1
	C1 = np.zeros([2,2])
	C1[0,0] = 1
	C2 = np.zeros([2,2])
	C2[1,1] = 1 
	while len(C1)<len(U):
		if cWire < oWire:
			C1 = np.kron(C1,I)
		else:
			C1 = np.kron(I,C1)

	for i in range(diff):
		if cWire< oWire:
			C1 = np.kron(C1,I)
			CH = np.kron(C2,CH)
		else:
			C1 = np.kron(I,C1)
			CH  = np.kron(CH,C2)

	CH = C1 + CH

	# # if cWire<oWire:
	# # 	CH = controlU(U,diff,1)
	# # else:
	# # 	CH = controlU(U,diff,0)
	CN = 1
	l=0
	while l < totalwires:
		if l==cWire or l==oWire:
			CN=np.kron(CN,CH)
			if cWire>oWire:
				l=cWire+1
			else:
				l=oWire+len(U)+1
			continue
		l+=1
		CN= np.kron(CN,I)	
	return CN

def QFTArray(i,k,totalwires,undof=0):
	Q = UQFT(k)
	I = np.eye(2)
	QF = 1
	l=0
	while l< totalwires:
		if l==i:
			QF=np.kron(QF,Q)
			l+=k
			continue
		else:
			QF=np.kron(QF,I)
		l+=1
	if undof:
		return np.linalg.inv(QF)



def UQFT(totalwires):
	w = np.arange(2**totalwires,dtype=complex)
	a=[]
	for i in range(2**totalwires):
		a.append([np.exp(1j*2*np.pi*i*x/totalwires) for x in w])
	return 1.0/np.sqrt(2**totalwires)*np.asarray(a)

def tofelli(c1,c2,o,numwire):
	U=[]
	nw = abs(c1-0) + 1 
	U.append(HadamardArray(o, numwire))
	U.append(CPhaseArray(c2,o,np.pi/2,numwire))
	U.append(CNOTArray(c1, c2,numwire))
	U.append(np.matrix(CPhaseArray(c2,o,np.pi/2,numwire)).getH())
	U.append(CNOTArray(c1, c2,numwire))
	U.append(CPhaseArray(c1,o,np.pi/2,numwire))
	U.append(HadamardArray(o, numwire))
	fnalmat=1
	for mat in U:
		fnalmat=np.dot(mat,fnalmat)
	return fnalmat

if __name__ == '__main__':
	U = xyModN(3,15,4)
	print CUArray(U,0,1,5)

	# print np.dot(A,tofelli(0,1,2,3))

	#U = xyModN(2, 15, 5)

	#def controlf(U,cWire,oWire,numWire):


	# A = np.zeros(2**2)
	# A[2] = 1
	# A[3] = 1
	# print np.dot(CNOTArray(0,1,2),A)





	# A = np.zeros(2**3)
	# A[4] = 1
	# #print np.dot(A,CNOTArray(2,1,3))

	# print np.dot(CNOTArray(2,1,3,1),CNOTArray(2,1,3))
	# #print np.dot(A,HadamardArray(2,3))


	# print np.dot(A,PhaseArray(0.785,0,3))
	# S=[]
	# for i in range(8):
	# 	k= [int(x) for x in bin(i)[2:]]
	# 	for l in range(8):
	# 		j= [int(l) for l in bin(l)[2:]]
	# 		S.append(U(k,j,3))

	# out = 1.0/np.sqrt(8)*np.asarray(S).reshape([8,8])

	# print UQFT(3)-out#U = xyModN(2, 15, 5)

	#def controlf(U,cWire,oWire,numWire):


	# A = np.zeros(2**3)
	# A[0] = 1
	# print np.dot(UQFT(3),A)





	# A = np.zeros(2**3)
	# A[4] = 1
	# #print np.dot(A,CNOTArray(2,1,3))

	# print np.dot(CNOTArray(2,1,3,1),CNOTArray(2,1,3))
	# #print np.dot(A,HadamardArray(2,3))


	# print np.dot(A,PhaseArray(0.785,0,3))
	# S=[]
	# for i in range(8):
	# 	k= [int(x) for x in bin(i)[2:]]
	# 	for l in range(8):
	# 		j= [int(l) for l in bin(l)[2:]]
	# 		S.append(U(k,j,3))

	# out = 1.0/np.sqrt(8)*np.asarray(S).reshape([8,8])

	# print UQFT(3)-out