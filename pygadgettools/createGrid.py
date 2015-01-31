###NAME: createGrid.py
###PURPOSE: all grid related functions

import numpy as np

def gridAround(x):
    """
    PURPOSE: return the midpoint between 2 pairs of number with fixed boundary.
    EXEMPLE:
    x = array([ 0. ,  0.1,  0.2,  0.3,  0.4,  0.5,  0.6,  0.7,  0.8,  0.9])
    return >> array([ 0.  ,  0.05,  0.15,  0.25,  0.35,  0.45,  0.55,  0.65,  0.75, 0.85,  0.9 ])
    """

    nr=len(x)
    dr=np.diff(x)
    ndr=len(dr)
    coradius=np.zeros(nr+1)
    nrco=len(coradius)
    
    coradius[0]=x[0] #start coradius = start radius
    coradius[nrco-1]=x[nr-1] #end coradius = end radius
    coradius[1:nrco-1]=x[0:nr-1]+dr[0:ndr]/2. #take half distance

    return coradius

def midPoint(x):
    """
    PURPOSE: return the midpoint between 2 pairs of number
    EXEMPLE:
    x = array([ 0. ,  0.1,  0.2,  0.3,  0.4,  0.5,  0.6,  0.7,  0.8,  0.9])
    return >> array([ 0.05,  0.15,  0.25,  0.35,  0.45,  0.55,  0.65,  0.75,  0.85])
    """
    return (x[1:] + x[:-1]) / 2


