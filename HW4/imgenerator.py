#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
	newim1 = np.identity(10,dtype=int)
	for i in range(10):
		newim1[i,9-i] = 1
	np.savetxt('10x10im1',newim1.flatten(),fmt='%d',delimiter='',newline='')
	# plt.matshow(newim1)
	# plt.show()
	newim2 = np.zeros([10,10])
	for i in range(10):
		newim2[i,5] = newim2[5,i] = 1
	np.savetxt("10x10im2",newim2.flatten(),fmt='%d',delimiter='',newline='')
	# plt.matshow(newim2)
	# plt.show()
	newim3 = np.zeros([10,10])
	for i in range(10):
		newim3[i,2]=newim3[i,6]=newim3[2,i]=newim3[6,i]=1
	np.savetxt("10x10im3",newim3.flatten(),fmt='%d',delimiter='',newline='')
	# plt.matshow(newim3)
	# plt.show()
