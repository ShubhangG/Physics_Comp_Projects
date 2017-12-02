#Circuit generator
import sys
import math
import numpy as np
import pickle as pk 
import matplotlib.pyplot as plt

def writetofile(x,N):
	w = int(math.ceil(math.log(N,2)))
	n = 3*w
	f = open("QntShor", "wb")
	f.write(repr(n)+'\n')
	f.write("INITSTATE FILE shorinput\n")
	ctr=0
	for i in range(n-w):
		f.write("H "+repr(i))
		f.write('\n')
	for i in range(n-w):
			for k in range(2**(i+1)):
				f.write("CFUNC "+repr(n-w-i-1)+" " +repr(n-w)+" "+ repr(w)+" " + "xyModN " + repr(x)+" " + repr(N))
				f.write('\n')
				ctr+=1
	f.write("undoQFT "+ repr(0) + " " + repr(n-w-1)+"\n")
	f.write("Measure")
	ctr+=1
	f.close()
	f1 = open("shorinput","wb")
	u = np.zeros(2**(2*w),dtype=complex)
	u[0] = 1
	ps = np.zeros(2**w,dtype=complex)
	ps[1] = 1
	out = np.kron(ps,u)
	print len(out)
	for k in out:
		f1.write(repr(np.real(k))+" "+repr(np.imag(k))+"\n")
	#np.savetxt(f1,out.reshape(1,out.shape[0]),newline='\n',fmt = '%.4e')
	f1.close()
	return ctr+n-w


N = input("Enter the number you want to factor: ")
x = input("Enter x: ")
writetofile(x,N)
# a= []
#b = np.arange(2,100)
# for k in range(2,100):
# 	a.append(writetofile(2,k))

#pk.dump(a, open("largenumberofgates.pk", "wb"))

# a = pk.load(open("largenumberofgates.pk","rb"))
# plt.loglog(b,a)
# plt.xlabel("log(N)")
# plt.ylabel("log(Number of gates)")
# plt.title("Growth of Shor size plot")
# plt.savefig("QntmShorgrowth.png")
# plt.show()
# plt.close()
