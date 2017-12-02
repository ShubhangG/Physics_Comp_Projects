import numpy as np 
import random
from datetime import datetime

random.seed(datetime.now())
fgate  = open("randgate","wb")
numwire = random.randrange(1,10)
fgate.write(repr(numwire) + "\n")
numH = random.randrange(5)
numP = random.randrange(5)
numCnot = random.randrange(5)
undo = []


Hctr=0
Pctr=0
Cnotctr=0
while Hctr<numH or Pctr<numP or Cnotctr<numCnot: 
	tok =random.randrange(3)
	if tok==0:
		if Hctr==numH:
			continue
		k = random.randrange(numwire)
		fgate.write("H "+repr(k)+'\n')
		undo.append("undoH " + repr(k) + '\n')
		Hctr+=1
	elif tok==1:
		if Pctr==numP:
			continue
		l = random.randrange(numwire)
		theta = random.uniform(0,2*np.pi)
		fgate.write("P " + repr(l) + " "+ repr(theta)+ "\n")
		undo.append("undoP " + repr(l) + " "+ repr(theta) + '\n')
		Pctr+=1
	else:
		if Cnotctr==numCnot:
			continue
		CO = random.sample(range(numwire),2)
		fgate.write("CNOT "+ repr(CO[0]) + " "+ repr(CO[1])+ "\n")
		undo.append("undoCNOT "+ repr(CO[0]) + " "+ repr(CO[1])+ "\n")
		Cnotctr+=1

Unum = np.asarray(undo)
reversedundo = Unum[::-1]
for gate in reversedundo:
	fgate.write(gate)

fgate.close()





