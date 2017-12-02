from ParseInput import *

def fHadamardArray(inWire,numWires,inputState):
	outputState=np.zeros(2**numWires,dtype=complex)
	for i in range(2**numWires):
		if inputState[i]:
			porm=1.0
			v = state2vec(i,numWires)
			#print v
			k = v[:]
			j= v[:]
			if v[inWire]:
				porm = -1.0
			k[inWire] = 1
			j[inWire] = 0
			#print j
			#print k
			outputState[vec2state(k)] =  outputState[vec2state(k)]+porm
			outputState[vec2state(j)]= outputState[vec2state(j)]+1.0
	return outputState/np.linalg.norm(outputState)
def state2vec(numstate,numwire):
	vec = [int(l) for l in bin(numstate)[2:]]
	if len(vec)<numwire:
		for i in range(numwire-len(vec)):
			vec = [0] + vec
	return vec

def vec2state(vec):
	bstr = ''.join(map(str,vec))
	return int(bstr,2)

def fCNOTArray(cWire, oWire,numWires,inputState):
	outputState=np.zeros(2**numWires,dtype=complex)
	for i in range(2**numWires):
		if inputState[i]:
			v = state2vec(i,numWires)
			if v[cWire]:
				if v[oWire]:
					v[oWire]=0
				else:
					v[oWire]=1
				outputState[vec2state(v)] = outputState[vec2state(v)] + 1.0
			else:
				outputState[i] = inputState[i]
	return outputState/np.linalg.norm(outputState)

def fphase(inWire,numWires, theta, inputState):
	outputState=np.zeros(2**numWires,dtype=complex)
	for i in range(2**numWires):
		if inputState[i]:
			v = state2vec(i,numWires)
			if v[inWire]:
				outputState[i] = outputState[i] + np.exp(1j*theta)
			else:
				outputState[i] = inputState[i]
	return outputState/np.linalg.norm(outputState)

def cntrlfphase(cWire,inWire,numWires, theta, inputState):
	outputState=np.zeros(2**numWires,dtype=complex)
	for i in range(2**numWires):
		if inputState[i]:
			v = state2vec(i,numWires)
			if v[cWire]:
				if v[inWire]:
					outputState[vec2state(v)] = outputState[vec2state(v)] + np.exp(1j*theta)
				else:
					outputState[vec2state(v)] = inputState[vec2state(v)]
			else:
				outputState[i] = inputState[i]
	return outputState/np.linalg.norm(outputState)
# def fCntrlxymodN(cWire,inWire,numWires,inputState):
# 	outputState

# fCNOTArray(0,1,2,[1,0,0,0])
# fphase(1,2,np.pi/2,[0,0,0,1])