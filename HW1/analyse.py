import numpy as np
from glob import glob
import matplotlib.pyplot as plt
import re
import gzip
import shutil
import os

# Sort_nicely taken from https://blog.codinghorror.com/sorting-for-humans-natural-sort-order/
def sort_nicely( l ):  
	""" Sort the given list in the way that humans expect.
	"""
	convert = lambda text: int(text) if text.isdigit() else text
	alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
	l.sort( key=alphanum_key )

def neighbour(dat, x, y): 	#checks the neighbouring data points and averages em
	avg= 0.0
	ctr=0
	#look up
	if(x!=0):
		avg= avg+ dat[x-1,y] #top
		ctr+=1
		if(y!=0):
			avg=avg+ dat[x-1,y-1] + dat[x,y-1] #left and topleft
			ctr+=2
		if(y!=len(dat)-1):
			avg=avg+dat[x,y+1]+dat[x-1,y+1] #right and topright
			ctr+=2
	#look down
	if(x!=len(dat)-1):
		avg = avg+dat[x+1,y] #down
		ctr+=1
		if(y!=0):
			avg=avg+ dat[x+1,y-1] + dat[x,y-1] #left and bottomleft
			ctr+=2
		if(y!=len(dat)-1):
			avg=avg+dat[x,y+1]+dat[x+1,y+1] #right and bottomright
			ctr+=2
	return round(avg/ctr*2)/2



def coarse_grain(dat):		#Run coarse graining
	coarse_dat = np.zeros_like(dat)
	for i in range(len(dat)):
		for j in range(len(dat)):
			coarse_dat[i,j] = neighbour(dat, i, j)
	return coarse_dat

def create_snapshots():		#Snapshots for coarsed and fine
	fnames = glob('snap_*')
	sort_nicely(fnames)
	arrays = [np.loadtxt(f) for f in fnames]
	fnal = np.asarray(arrays)
	imgdim = int(np.sqrt(len(fnal[0])))
	ctr=0;
	for tstep in fnal:
		 dat = np.zeros((imgdim,imgdim))
		 for val in tstep:
			j = np.asarray(val).astype(int)
		 	dat[j[0],j[1]] = j[2]
		 plt.matshow(dat)
		 plt.savefig("shot_"+repr(ctr)+".png")
		 plt.close()
		 plat = coarse_grain(dat)
	 	 plt.matshow(coarse_grain(plat))
	 	 plt.savefig("coarse_"+repr(ctr)+".png")
	 	 plt.close()
	 	 ctr+=1

def entropy():			#measures entropy
	fnames = glob('shot_*')
	fnames2 = glob('coarse_*')
	entr=[]
	cmplx=[]
	sort_nicely(fnames)
	sort_nicely(fnames2)
	ctr=0

	for f in fnames:
		with open(f,'rb') as f_in:
			with gzip.open("entr_"+repr(ctr)+".txt.gz", "wb") as f_out:
				shutil.copyfileobj(f_in,f_out)
		entr.append(os.path.getsize("entr_"+repr(ctr)+".txt.gz"))
		ctr+=1
	ctr=0
	for f2 in fnames2:
		with open(f2,'rb') as f_in:
			with gzip.open("cmplx_"+repr(ctr)+".txt.gz", "wb") as f_out:
				shutil.copyfileobj(f_in,f_out)
		cmplx.append(os.path.getsize("cmplx_"+repr(ctr)+".txt.gz"))
		ctr+=1
	xaxis = np.arange(len(fnames))
	plt.plot(xaxis,entr, label="Entropy")
	plt.plot(xaxis,cmplx, label="complexity")
	plt.title("Entropy and complexity Plot")
	plt.xlabel("time steps x10^6")
	plt.ylabel("size of gzip file")
	plt.legend()
	plt.savefig("Entropy_cmplx_calc.png")
	plt.show()

create_snapshots()
entropy()
