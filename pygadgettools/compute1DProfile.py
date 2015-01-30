###NAME: compute1DProfile.py
###PURPOSE: compute 1D Profile along an axis

import numpy as np
import createGrid




def mean(x,q,radius):
    """
    PURPOSE: compute the mean of the quantity q(x) as function of radius
    INPUTS: x = position
            q = quantity to be averaged
            radius = location at which you want the mean.
    COMMENTS: this is a very slow function. I optimized already a bit, but maybe we can do even better...
    """

    nr=np.size(radius)
    coradius=createGrid.gridAround(radius)
    

    #copy original values
    xx=np.copy(x)
    qq=np.copy(q)
    meanq=np.zeros(nr)
    for i in range(0,nr):
        sublist=(xx>=coradius[i]) & (xx<coradius[i+1])
        meanq[i]=np.mean(qq[sublist])

        #remove from the list already used data (for speedup)
        qq=qq[np.logical_not(sublist)] 
        xx=xx[np.logical_not(sublist)]
                         
    return meanq



def min(x,q,radius):
    """
    PURPOSE: compute the min of the quantity q(x) as function of radius
    INPUTS: x = position
            q = quantity to be averaged
            radius = location at which you want the mean.
    COMMENTS: this is a very slow function. I optimized already a bit, but maybe we can do even better...
    """

    nr=np.size(radius)
    coradius=createGrid.gridAround(radius)
    

    #copy original values
    xx=np.copy(x)
    qq=np.copy(q)
    meanq=np.zeros(nr)
    for i in range(0,nr):
        sublist=(xx>=coradius[i]) & (xx<coradius[i+1])
        meanq[i]=np.min(qq[sublist])

        #remove from the list already used data (for speedup)
        qq=qq[np.logical_not(sublist)] 
        xx=xx[np.logical_not(sublist)]
                         
    return meanq
