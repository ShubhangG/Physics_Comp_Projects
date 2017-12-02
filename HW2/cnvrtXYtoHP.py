import numpy as np 
import collections
from GateArrays import *

def ReadInput(fileName):
	lines = open(fileName).readlines()
	myInput = []
	numberOfWires=int(lines[0])
	for line in lines[1:]:
		myInput.append(line.split())
	return (numberOfWires,myInput)

def cnvrtXY(numWire, myinput):
	f = open("newinput","wb")
	f.write(repr(numWire)+"\n")
	for gate in myinput:
		if gate[0] == "X":
			f.write("H")





