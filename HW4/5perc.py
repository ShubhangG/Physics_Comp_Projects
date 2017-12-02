import numpy as np
import matplotlib.pyplot as plt

cmap=plt.get_cmap('gnuplot')
colors= [cmap(i) for i in np.linspace(0,1,10)]
for i, col in enumerate(colors,start=1):
	ener = np.loadtxt("outputs/out_"+repr(i))
	plt.plot(ener[:,0],ener[:,1],c=col)
plt.xlabel("Iteration")
plt.ylabel("Energy")
plt.title("I set a beta of 10 and 10 different configurations for 100 neurons")
plt.savefig("energred.png")
plt.show()
plt.close()