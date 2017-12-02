import numpy as np
import matplotlib.pyplot as plt

def corr(trace):
    """ calculate the autocorrelation of a trace of scalar data
    pre:  trace should be a 1D iterable array of floating point numbers
    post: return the autocorrelation of this trace of scalars 
    """

    correlation = 1.0
    su =0.0
    n = len(trace)
    for k in range(1,n):
        cc = compcorr(trace,k)
        if cc<=0:
            break
        su = su + cc
        
        

    correlation = 1 + 2*su
    return correlation

def compcorr(trace, k):
    R = 0.0
    n = len(trace)
    mu = np.mean(trace)
    sigma = np.std(trace)
    sigma = sigma**2
    for t in range(n-k):
        R = R + (trace[t] - mu)*(trace[t+k] - mu)
    
    R = R/((n-k)*sigma)
    return R

# end def corr

def error(trace):
    #stderr = 0.0
    N_eff = len(trace)/corr(trace)
    sigma = np.std(trace)
    stderr = sigma/np.sqrt(N_eff)
    # calculate standard error
    #print(sigma/len(trace))
    return stderr

def neighbour(dat, x, y):   #checks the neighbouring data points and averages em
    avg= 0.0
    ctr=0
    #look up
    if(x!=0):
        avg= avg+dat[x-1,y] #top
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
    if avg>0: 
        return 1
    else:
        return -1 

def coarse_grain(sshot):
    mat=np.loadtxt(sshot)
    cgrained = np.zeros([len(mat)/3,len(mat)/3])
    for y in range(len(cgrained)):
        for x in range(len(cgrained[0])):
            cgrained[x,y] = neighbour(mat,3*x+1,3*y+1)
    return cgrained


# ctr=1.0
# avg_m = 0.0
# for val in m:
#   if ctr%N_eff!=0:
#       ctr+=1
#       continue
#   avg_m+=val
#   ctr+=1

# print "Average using N_eff m^2: ", avg_m/ctr