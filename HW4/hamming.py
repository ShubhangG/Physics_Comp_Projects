import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
	hamdists = np.loadtxt("hammingdistances.txt")
	y = np.linspace(0,100,11)
	plt.imshow(hamdists.T,interpolation='hamming',aspect='auto')
	plt.gca().invert_yaxis()
	cbar = plt.colorbar()
	cbar.set_label("Hamming Distance")
	plt.xlabel("Number of memories")
	plt.ylabel("%/10 corruption")
	plt.savefig("Hammingdist.png")
	plt.show()
	#print len(hamdists[0])
