###NAME: profile.py
###PURPOSE: compute 1D Profile along an axis

import numpy as np
import geometry.create_grid as grid



def mean(x,q,radius):
    """Compute the mean of the quantity q(x) as function of radius

    Parameters:
    ----------
    
    x : float array
        position
        
    q : float array
        quantity to be averaged
        
    radius : float array
        location at which you want the mean.

    """

    ##this is a very slow function. I optimized already a bit, but maybe we can do even better...
    
    nr=np.size(radius)
    coradius=grid.gridAround(radius)
    

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
    """ Compute the min of the quantity q(x) as function of radius

    Parameters:
    ----------
    
    x : float array
        position
        
    q : float array
        quantity to be averaged
        
    radius : float array
        location at which you want the mean.
    
    """

    nr=np.size(radius)
    coradius=grid.gridAround(radius)
    

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


def n_in_shell(x,bins):
    """ Gives number of particles inside each bin

    Parameters:
    ----------
    
    x : float array
        position
          
    bins : float array
        bin limits

    """
        
    #copy original values
    xx=np.copy(x)
    nr=len(bins)-1 #number of intervals 
    nshell=np.zeros(nr)
    for i in range(0,nr):
        sublist   = (xx>=bins[i]) & (xx<bins[i+1])
        nshell[i] = np.count_nonzero(sublist)
        xx        = xx[np.logical_not(sublist)] #remove from the list already used data (for speedup)

    return nshell


def mass_per_shell(x,mass,bins):
    """ Gives number of particles inside each bin

    Parameters:
    ----------
    
    x : float array
        position

    mass : float array
        mass of each particle. Must be the same dimension than x.
                  
    bins : float array
        bin limits

    """

    xx=np.copy(x)
    mm=np.copy(mass)
    nr=len(bins)-1 #number of intervals 
    mass_bin=np.zeros(nr) #mass in each bin
    for i in range(0,nr):
        sublist   = (xx>=bins[i]) & (xx<bins[i+1])
        mass_bin[i] = np.sum(mm[sublist])
        xx        = xx[np.logical_not(sublist)] #remove from the list already used data (for speedup)
        mm        = mm[np.logical_not(sublist)] #remove from the list already used data (for speedup)

    return mass_bin


def enclosed_mass(x,mass,bins):
    """Compute the enclosed mass along an axis.

    Parameters:
    ----------
    
    x : float array
        position

    mass : float array
        mass of each particle. Must be the same dimension than x.
                  
    bins : float array
        bin limits

    """

    mass_shell=massPerShell(x,mass,bins) #compute mass in each shell
    total_mass=np.cumsum(mass_shell,dtype='float64')
    return total_mass



def spherical_densityDM(r,mass,radius):
    """Compute the radial density profile of DM.

    Parameters:
    ----------
    
    r : float array
        radial position of particles

    mass : float array
        mass of each particle. Must be the same dimension than r.
                  
    radius : float array
        radius along which you want the density profile

    """
    
    coradius=grid.gridAround(radius)
    mass_shell=mass_per_shell(r,mass,coradius) #mass per shell
    volume_shell=grid.sphericalvolume_per_shell(coradius) #volume per shell
    return mass_shell/volume_shell
