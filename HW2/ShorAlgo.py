import numpy as np
import random
from datetime import datetime
from fractions import gcd
import matplotlib.pyplot as plt 
from sympy.ntheory.primetest import isprime
from scipy.signal import savgol_filter
import math
from time import time

random.seed(datetime.now())
N=15
failure = 0 
def Shor(x,N):
	global failure
	if isprime(N):
		return N,1
	r=1.0
	# for k in range(2,int(math.ceil(np.log(N)/np.log(2)+1))):
	# 	if abs(round(N**(1.0/k))-N**(1.0/k))<1e-10:
	# 		print "One factor of ",N,"is ",round(N**(1.0/k))
	# 		return
	while(r<N):
		if gcd(x,N)!= 1:
			return gcd(x,N)
		if (x**r)%N !=1:
			r+=1
			continue
		if r%2!=0:
			failure+=1
			x = random.randrange(1,int(math.ceil(np.sqrt(N)))+1)
			r=1.0
			continue
		if (x**(r/2))%N==-1:
			failure+=1
			x = random.randrange(1,int(math.ceil(np.sqrt(N)))+1)
			r=1.0
			continue
		print "r", r
		return gcd(x**(r/2)+1,N), gcd(x**(r/2)-1,N)
		break

print Shor(random.randrange(1,int(np.sqrt(N))),N)
# f= []
# t=[]
# for N in range(5,200):
# 	fail = 0.0
# 	#print Shor(random.randrange(1,int(np.sqrt(N))),N)
# 	for x in range(500):
# 		failure =0
# 		startt = time()
# 		Shor(random.randrange(1,int(np.sqrt(N))),N)
# 		fail+=failure
# 		endt = time() - startt
# 	f.append(fail/500)
# 	t.append(endt/500)

# x = np.arange(5,200)
# fhat = savgol_filter(f, 31, 3)
# that = savgol_filter(t,31,3)
# plt.semilogx(x,fhat,c='r',label="failures smoothened")
# #plt.semilogx(x,f,label="failures unsmoothened")
# plt.xlabel("log(N)")
# plt.ylabel("failures")
# plt.title("Graph of failures")
# plt.legend()
# plt.savefig("fail.png")
# plt.show()
# plt.close()

# plt.plot(x,that,c='b',label="Time")
# plt.xlabel("log(N)")
# plt.ylabel("log(Elapsed time)")
# plt.title("Graph of time complexity")
# plt.legend()
# plt.savefig("timyshor.png")
# plt.show()
# plt.close()