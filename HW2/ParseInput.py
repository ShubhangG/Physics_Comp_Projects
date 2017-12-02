import numpy as np 
import collections
import pickle as pk 
from GateArrays import *
from fastergates import *
Number2factor = 0
####################################################################################
np.set_printoptions(suppress=True, linewidth=np.nan, threshold=np.nan)
def ReadInput(fileName):
	lines = open(fileName).readlines()
	myInput = []
	numberOfWires=int(lines[0])
	for line in lines[1:]:
		myInput.append(line.split())
	return (numberOfWires,myInput)

def readvec(filename):
	vec = np.loadtxt(filename).view(complex).T
	return vec

def MakeUnitary(numWire, myinput):
	U = {}
	ctr = 0
	inpvec=1
	rev_flag = 0
	for gate in myinput:
		if gate[0] == 'INITSTATE':
			inpvec=readvec(gate[2])
			continue
		if gate[0].lower()=='measure':
			print "Pickling!"
			pk.dump(fnalmat,open("Savefnalmat.p","wb"))
			psi = measure(U,numWire,inpvec)
			extractShor(psi,Number2factor)
			continue
		U[ctr] = switch_case(gate,numWire)
		ctr+=1
	oU = collections.OrderedDict(sorted(U.items(),reverse=True))
	rU = collections.OrderedDict(sorted(U.items()))
	# if rev_flag:
	# 	reverse																																																																																															
	fnalmat = 1
	for key,val in oU.items():
		fnalmat = np.dot(val,fnalmat)
	
	return fnalmat 

def switch_case(gate,numWire):
		global Number2factor
		if gate[0] == 'H':
			return HadamardArray(int(gate[1]), numWire)
		elif gate[0] == 'CNOT':
			return CNOTArray(int(gate[1]),int(gate[2]),numWire)
		elif gate[0] == 'undoCNOT':
			return CNOTArray(int(gate[1]),int(gate[2]),numWire,1)
		elif gate[0] == 'P':
			return PhaseArray(float(gate[2]),int(gate[1]),numWire)
		elif gate[0] == 'undoP':
			return PhaseArray(float(gate[2]),int(gate[1]),numWire,1)
		elif gate[0] == 'undoH':
			return HadamardArray(int(gate[1]), numWire,1)
		elif gate[0] == "CP":
			return CPhaseArray(int(gate[1]),int(gate[2]),float(gate[3]),numWire)
		elif gate[0] == "CFUNC":
			if gate[4] == "xyModN":
				Number2factor = int(gate[6]) 
				U = xyModN(int(gate[5]), int(gate[6]), int(gate[3]))
				# print len(U)
				# print np.linalg.eig(U)
				# assert 1==0
				# print np.linalg.eig(CUArray(U,int(gate[1]),int(gate[2]),numWire))
				# assert 1==0
				return CUArray(U,int(gate[1]),int(gate[2]),numWire)
		elif gate[0] == "X":
			return PXArray(int(gate[1]),numWire)
		elif gate[0] == "QFT":
			return QFTArray(int(gate[1]), int(gate[2]),numWire)
		elif gate[0] == "undoQFT":
			return QFTArray(int(gate[1]), int(gate[2]),numWire,1)
		elif gate[0] == "tofelli":
			return tofelli(int(gate[1]),int(gate[2]),int(gate[3]),numWire)
		elif gate[0] == "CU":
			U = []
			for k in range(3,7):
				if 'i' in gate[k]:
					gate[k].replace("i","")
					U.append(1j*int(gate[k]))
			U = np.asarray(U,dtype=complex).reshape([2,2])
			return CUArray(U,int(gate[1]),int(gate[2]),numWire)
		else:
			print "Gate DOES NOT EXIST!"
			return 1 

def measure(U,numWire,inpvec=1):
	oU = collections.OrderedDict(sorted(U.items(),reverse=True))
	fnalmat = 1
	for key,val in oU.items():
		#print key,len(val)
		fnalmat = np.dot(val,fnalmat)
	if type(inpvec) is int:
		inpvec = np.zeros(2**numWire)
		inpvec[0] = 1 

	return np.dot(inpvec,fnalmat) 

#Truncate taken from https://stackoverflow.com/questions/783897/truncating-floats-in-python
def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '%.12f' % f
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])

def extractShor(psi,N):
	#print N
	if N==0:                                               
		print psi
		return
	npsi = np.absolute(psi[:2**(2*N)])
	#print npsi[0][0]
	#print npsi
	npsi=npsi[0].tolist()
	npsi[0]=0.0
	midx = npsi.index(max(npsi))
	mval = max(npsi)

	print midx
	#print mval
	binidx = [int(l) for l in bin(midx)[2:]]
	sor = vec2state(binidx[0:7])
	print binidx
	#sor = 1.0*float(midx)/2**(2*N)
	#print sor
	#print float(round(sor,5)).as_integer_ratio()
	# npsi = psi/np.linalg.norm(psi)
	# k = []
	# for x in np.nditer(npsi[0:N]):
	# 	if x!=0:
	# 		k.append(1)
	# 	else:
	# 		k.append(0)
	# bstr = ''.join(map(str,k))
	# dec = 1.0*int(bstr,2)/2**(len(k))
	# print float(truncate(dec,1)).as_integer_ratio()[1]
	return #dec.as_integer_ratio()[1] 

def fastparse(nwire, gates):
	inpvec = np.zeros(2**nwire)
	inpvec[0] = 1
	outputState= inpvec[:]
	for gate in gates:
		if gate[0] == 'INITSTATE':
			inpvec=readvec(gate[2])
			continue
		if gate[0] == 'H':
			outputState = fHadamardArray(int(gate[1]),nwire,outputState)
		elif gate[0] == 'CNOT':
			outputState = fCNOTArray(int(gate[1]), int(gate[2]),nwire,outputState)
		elif gate[0] == 'P':
			outputState = fphase(int(gate[1]),nwire, float(gate[2]), outputState)
		elif gate[0].lower() == 'measure':
			return outputState
	return
###########################################################################


if __name__ == '__main__':
	nwire, gates = ReadInput("QntShor")
	#nwire, gates = ReadInput("myGate")
	MakeUnitary(nwire,gates)
	#print "Faster\n", fastparse(nwire,gates)

# A=np.zeros(2**nwire)
# A[0] = 1
# print np.dot(A,MakeUnitary(nwire,gates))
# A = [0,np.sqrt(0.25),0,np.sqrt(0.5),0,np.sqrt(0.25),0,0]
# print np.linalg.norm(np.dot(A,MakeUnitary(nwire,gates)))
# print MakeUnitary(nwire,gates)