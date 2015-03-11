###NAME: create_grid.py
###PURPOSE: all grid related functions

import numpy as np



def grid_around(x):
    """Return the midpoint between 2 pairs of number with fixed boundary.

    Parameters:
    ----------

    x : float array
       The array along which you want the grid

    Example:
    -------
    
    >>> grid_around(np.arange(0,10))
    array([ 0. ,  0.5,  1.5,  2.5,  3.5,  4.5,  5.5,  6.5,  7.5,  8.5,  9. ])

    """


    ### I could probably change this function and create instead a method to create a grid around a numpy array, somethings like x.grid_around('mid')
    
    nr=len(x)
    dr=np.diff(x)
    ndr=len(dr)
    coradius=np.zeros(nr+1)
    nrco=len(coradius)
    
    coradius[0]=x[0] #start coradius = start radius
    coradius[nrco-1]=x[nr-1] #end coradius = end radius
    coradius[1:nrco-1]=x[0:nr-1]+dr[0:ndr]/2. #take half distance

    return coradius



def midpoints(x):
    """Return the midpoint between 2 pairs of number
    
    Parameters:
    ----------

    x : float array
       The array along which you want the grid

    Example:
    -------
    
    >>> midpoints(np.arange(0,5))
    array([ 0.5,  1.5,  2.5,  3.5])
    
    """
    return (x[1:] + x[:-1]) / 2.


def volume_per_shell(bins):
    '''
    PURPOSE : return the volume inside each shell around the radius location (boundary= half distance with next points)
    INPUTS : radius = input array of location of each radial point
    OUTPUTS : volume_per_shell = volumen inside each shell whose center is given by radius
    '''

    def volume_sphere(r):
        return 4./3.*np.pi*r**3


    #we calculate the larger sphere and we substract the inside sphere to get the volume of the shell
    
    nr=len(bins) #number of bins
    sphere=volume_sphere(bins)
    volume_per_shell=sphere[1:]-sphere[0:nr-1]
    
    return volume_per_shell
