#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
	b4 = np.loadtxt('snapshot/smilb4.dat')
	aft = np.loadtxt('snapshot/smilafter.dat') 
	stateb4 = b4[:,0]
	stateaft = aft[:,0]
	#print stateb4
	weight = b4[:,1:]
	#print weight.reshape((100,100))
	plt.matshow(stateb4.reshape((10,10)))
	plt.savefig("b4hopk29(1).png")
	plt.show()
	plt.close()

	plt.matshow(stateaft.reshape((10,10)))
	plt.savefig("afthopk29(1).png")
	plt.show()
	plt.close()
