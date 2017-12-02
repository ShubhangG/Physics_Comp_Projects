import numpy as np
import math
import pickle as pk
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from PAnalysis import *
import os

currdir = os.path.dirname(os.path.abspath(__file__))
def plot_snapshot(filename,beta):
	mat = np.loadtxt(filename)
	plt.matshow(mat)
	plt.savefig(currdir+"/plot/snap_"+repr(beta)+".png")
	plt.show()
	plt.close()

def plot_E(filename,beta):
	E = np.loadtxt("outputs/"+filename)
	plt.plot(E[:,0],E[:,1])
	plt.xlabel("Configuration number")
	plt.ylabel("Energy")
	plt.title("Energy distribution for beta = "+repr(beta))
	plt.savefig(currdir+"/plot/distr_"+repr(beta)+".png")
	plt.show()
	plt.close()

def plot_config(filename,beta,num):
	cnifgs = np.loadtxt(filename,dtype=int)
	#plt.plot(cnifgs[:num+1,0],cnifgs[:num+1,1])
	x = np.arange(511)
	y = savgol_filter(np.bincount(cnifgs[:,1]),51,3)
	plt.plot(x,y)
	plt.ylabel("bin_count")
	plt.xlabel("Config_num")
	plt.title("configuration distribution for beta = "+repr(beta))
	plt.savefig(currdir+"/plot/configdistr"+repr(num)+"_"+repr(beta)+".png")
	plt.show()
	plt.close()

def Getmandplotm(filename,beta):
	mnE = np.loadtxt("outputs/"+filename)
	m = mnE[:,1]
	E = mnE[:,2]
	err = error(m)
	N_eff = int(math.floor(len(m)/corr(m)))
	#print "Effective N", N_eff

	#print "Average m^2: ",np.sum(m[::N_eff])/N_eff
	#print "error in average m^2 is: ", err


	plt.plot(m[::N_eff])
	plt.xlabel("iteration*"+repr(N_eff))
	plt.ylabel("m^2")
	plt.title("Plotting magnetization of Ising Model")
	plt.savefig("plot/sim_exp_mPlot"+repr(beta)+".png")
	plt.show()
	plt.close()

	plt.plot(E[::N_eff])
	plt.xlabel("iteration*"+repr(N_eff))
	plt.ylabel("E")
	plt.title("Plotting Energy of ising")
	plt.savefig("plot/sim_exp_Eplot"+repr(beta)+".png")
	plt.show()
	plt.close()
	return np.sum(m[::N_eff])/len(m[::N_eff]), err
#plot_config("Whichconfig_500.dat",0.15,500)
def mvsbeta():
	beta = np.linspace(0.1,0.9,9)
	msq = [1.38620538005e-05,2.56303018347e-05,6.14149523332e-05,5.14576936469e-05,0.000132892930043,0.000214117123135,0.000335458342493,0.000433836219548,0.00061813745425]
	merr = [0.000244023283979,0.000328440966003,0.000432129153963,0.000559537164345,0.000685420975269,0.000853654025751,0.00107112717524,0.00119879208687,0.00142082517274]
	plt.errorbar(beta,msq,yerr=merr,capthick=3)
	plt.title("<m^2> vs beta plot for 2D 5x5 Ising model")
	plt.xlabel("Beta")
	plt.ylabel("<m^2>")
	plt.savefig(currdir+"/plot/m2vsbeta5x5.png")
	plt.show()

def snapcoarsegrain(filename,beta):
	cgrain = np.loadtxt(filename)
	ctr=len(cgrain)
	while(ctr>=3):
		plt.matshow(cgrain)
		plt.savefig(currdir+"/plot/b"+repr(beta)+"_plotof_"+repr(ctr)+"X"+repr(ctr)+".png")
		plt.close()
		np.savetxt(currdir+"/grain_dat/b"+repr(beta)+"_graining"+repr(ctr)+".dat",cgrain)
		filename = "grain_dat/b"+repr(beta)+"_graining"+repr(ctr)+".dat"
		cgrain = coarse_grain(filename)
		ctr = ctr/3
		 
def plotM(sshot,beta,cg=0):
	Mvals = []
	for i in range(100):
		sht= "snap_dats/"+sshot+"_"+repr(i)+".dat"
		if(not cg): redising = coarse_grain(sht)
		else: redising = np.loadtxt(sht)
		Mvals.append(np.abs(1.0*redising.sum()/redising.size))
	plt.plot(np.arange(100),np.abs(Mvals))
	plt.xlabel("Step number*10^5")
	plt.ylabel("P(|M|)")
	if(not cg): plt.title("Probability curve of M for coarse_grain Ising")
	else: plt.title("Probability curve of M for 27x27 Ising, beta="+repr(beta))
	plt.savefig(currdir+"/plot/"+sshot+"_"+repr(cg)+".png")
	plt.close()
	return np.std(Mvals)

def stdplotM():
	#std27 = [0.0115226337449,0.0148148148148,0.0136651955066,0.0169141976865]
	betavec = [0.33,0.38,0.4,0.45,0.5,0.55,0.6,0.65]
	std27 = [0.0291326506501,0.0353909465021,0.0396279178826,0.0294832026829,
	0.0224161297293,0.0260977316663,0.0406822727334,0.0351123111238]#0.016914]
	std81red = 0.037056338008
	plt.plot(betavec,std27,label="Ising 27x27")
	plt.axhline(std81red,c='r',label="Ising 81x81 coarse grained")
	plt.ylabel("standard deviations")
	plt.xlabel("beta J's")
	plt.title("Renormalization P(|M|) comparisons")
	plt.legend()
	plt.savefig(currdir+"/plot/stddevcmp.png")
	plt.show()

def Rjplot():
	rj = [0.33,0.34,0.46]
	xbeta = [0.2,0.32,0.4]
	plt.scatter(xbeta,rj,label="R(J)")
	plt.plot(xbeta,xbeta)
	plt.xlabel("beta J's")
	plt.ylabel("betaJ's after coarse graining")
	plt.title("R(J) vs J graph")
	plt.legend(loc=2)
	plt.savefig("RjvsJscatter.png")
	plt.show() 

#snapcoarsegrain("snap_dats/snap_0.300000.dat",0.3)
#Getmandplotm("simann_exp_out_2",0.2)
betiter = np.linspace(1,12,12,dtype=int)
#print betiter
#mvsbeta()
# m = []
# merr = []
# for i in betiter:
# 	val, err = Getmandplotm("out_"+repr(i),1.0*i/10.0)
# 	m.append(val)
# 	merr.append(err)

# betiter=1.0*betiter/10.0
# pk.dump((m),open("m2savefor27.pk","wb"))
# plt.plot(betiter,m)
# plt.xlabel("beta")
# plt.ylabel("magnetization <m^2>")
# plt.title("<m^2> vs beta plot for 2D 27x27 Ising model")
# plt.savefig(currdir+"/plot/m2vsbeta27x27.png")
# plt.show()
# M = []
# for i in betiter:
# 	M.append(plotM("snap_"+repr(i),1.0*i/10.0,1))

# pk.dump(M,open("Magsavefor27.pk","wb"))
# plt.plot(betiter/10.0,M)
# plt.xlabel("beta")
# plt.ylabel("STD DEV")
# plt.title("Std dev for different beta values for 27x27")
# plt.savefig("ProbM27x27.png")
# plt.show()
# plt.close()
#snapcoarsegrain("snap_dats/snap_12.dat",1.2)
#plotM("snap_1.250000",1.25,1)
#stdplotM()
#Rjplot()
