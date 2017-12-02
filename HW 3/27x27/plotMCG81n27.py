import pickle as pk
import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib import cm
import pandas as pd 
import scipy.optimize as optimize
import scipy.interpolate as interpolate
#from scipy.interpolate import interp1d


M27 = pk.load(open("Magsavefor27.pk","r"))[:5]
M81 = pk.load(open("msqrdagsaveforcgrain81.pk","r"))
colour = cm.rainbow(np.linspace(0,1,5))
betiter = np.linspace(0.1,0.5,5)
plt.plot(betiter,M27,label="Ising 27x27")
plt.plot(betiter,M81,label="CG 81x81 to 27x27")
plt.xlabel("beta values")
plt.ylabel("P(|M|)")
plt.title("coarse grain plotted on top 27x27")
plt.legend()
plt.savefig("plot1ontopofother.png")
plt.show()
plt.close()
#assert 1==0
fineriter = np.linspace(0.1,0.5,50)
ctr=0
# for std,c in zip(M81,colour):
# 	plt.axhline(std,c=c,label="Coarse_grained 81 beta="+repr(round(10*betiter[ctr])/10))
# 	ctr+=1

# plt.title("Finding R(J) and plotting results")
# plt.xlabel("beta value")
# plt.ylabel("P|M| std dev")
# plt.legend()
# plt.savefig("linedup81n27.png")
# plt.show()
# plt.close()

p27 = interpolate.interp1d(betiter,M27,kind='cubic')
p81 = interpolate.interp1d(betiter,M81,kind='cubic')

mm27 = p27(fineriter)
mm81 = p81(fineriter)
#plt.plot(fineriter,p27(fineriter))
#plt.show()
#p81 = interpolate.PiecewisePolynomial(betiter,M81[:,np.newaxis])
#assert 0
Mdic={}

for i in range(len(mm81)):
	Mdic[fineriter[i]]= fineriter[np.argwhere(np.diff(np.sign(mm27-mm81[i])) != 0).reshape(-1) + 0]

Mdic = {k:v for k,v in Mdic.iteritems() if v.any()}
print Mdic
u=[]
mvals = []
for k,v in Mdic.iteritems():
	a=np.empty(len(v),dtype=float)
	a.fill(k)
	u = np.append(u,a)
	#print u
	mvals = np.append(mvals,v)

# print len(u)
# print len(mvals)
# print u
# print mvals

uu = np.unique(u)
umval = np.unique(mvals)
addval = np.empty(np.abs(len(uu)-len(umval)))
addval.fill(2*umval[-1]-umval[-2])
umval = np.append(umval,addval)
print len(umval)
print len(uu)
#assert 1==0
plt.scatter(uu,umval[:len(uu)])
plt.xlabel("beta from 81 x81")
plt.ylabel("Coarse grained R(J)")
plt.title("R(J) vs J")
plt.savefig("RjvsJ_4.png")
plt.show()

#print u
#print mvals

# Mdf = pd.DataFrame(dict([(k,pd.Series(v)) for k,v in Mdic.iteritems()]))
#xs, ys = zip(*((x,k) for k in Mdic for x in Mdic[k]))
# xbeta = sorted(Mdic)
# a = []
# for k,v in Mdic.iteritems():
# 	a.append(np.empty(len(v)).fill(k))




# plt.scatter(x,y)
# plt.xlabel("beta from 81 x81")
# plt.ylabel("Coarse grained R(J)")
# plt.title("R(J) vs J")
# plt.savefig("RjvsJ.png")
# plt.show()