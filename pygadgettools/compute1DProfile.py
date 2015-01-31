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


def nShell(x,bins):
    '''
    PURPOSE : gives number of particles inside each bin
    INPUT : x = position
            bins = bin limits
    OUTPUTS : nshell = number of particles within each bin
    '''
        
    #copy original values
    xx=np.copy(x)
    nr=len(bins)-1 #number of intervals 
    nshell=np.zeros(nr)
    for i in range(0,nr):
        sublist   = (xx>=bins[i]) & (xx<bins[i+1])
        nshell[i] = np.count_nonzero(sublist)
        xx        = xx[np.logical_not(sublist)] #remove from the list already used data (for speedup)

    return nshell


def massPerShell(x,mass,bins):
    '''
    PURPOSE: computes the total mass enclosed in each bin
    INPUTS : x = position
             mass = mass of particles
             bins = bin limits
    OUTPUTS: mass per shell
    '''

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


def enclosedMass(x,mass,bins):
    '''
    PURPOSE: compute the enclosed mass along an axis
    INPUTS : x = position 
             mass = mass of particles
             bins = bin limits
    '''

    mass_shell=massPerShell(x,mass,bins) #compute mass in each shell
    total_mass=np.cumsum(mass_shell,dtype='float64')
    return total_mass



def sphericalDensityDM(r,mass,radius):
    """
    PURPOSE: compute 1D spherical density of DM
    INPUTS: r = radial position
            mass = mass of particles
            radius = radius along which you want the profile
    """

    coradius=createGrid.gridAround(radius)
    mass_per_shell=massPerShell(r,mass,coradius)
    volume_per_shell=createGrid.volumePerShell(coradius)
    return mass_per_shell/volume_per_shell
