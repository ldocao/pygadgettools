###NAME: computePhysics.py
###PURPOSE: compute some interesting physical quantities

import numpy as np
import pdb,sys
import changeCoordinates


### ANGULAR MOMENTUM
def specificAngularMomentum_cartesian(pos,vel):
    """
    PURPOSE : compute the value of specific angular momentum in gadget units
    INPUTS : pos = cartesian coordinates in gadget format (from readsnap)
             vel = cartesian velocity (must be same dimension than pos)
             """

    #save cartesian position of each particle
    x=pos[:,0]
    y=pos[:,1]
    z=pos[:,2]

    vx=vel[:,0]
    vy=vel[:,1]
    vz=vel[:,2]
    

    jx=(y*vz-z*vy)
    jy=(z*vx-vz*x)
    jz=(x*vy-vx*y)

    return np.dstack((jx,jy,jz))[0]


def specificAngularMomentum_cylindrical(pos,vel):
    """
    PURPOSE : compute the value of specific angular momentum in gadget units
    INPUTS : pos = cartesian coordinates in gadget format (from readsnap)
             vel = cartesian velocity (must be same dimension than pos)
    """

    r=pos[:,0]
    theta=pos[:,1]
    z=pos[:,2]

    vr=vel[:,0]
    vtheta=vel[:,1]
    vz=vel[:,2]

    jr= -vtheta*z
    jtheta=vr*z - vz*r
    jz=vtheta*r

    return np.dstack((jr,jtheta,jz))[0]


def specificAngularMomentum_spherical(pos,vel):
    """
    PURPOSE : compute the value of specific angular momentum in gadget units
    INPUTS : pos = cartesian coordinates in gadget format (from readsnap)
             vel = cartesian velocity (must be same dimension than pos)
    """

    r=pos[:,0]
    theta=pos[:,1]
    phi=pos[:,2]

    vr=vel[:,0]
    vtheta=vel[:,1]
    vphi=vel[:,2]

    jr= np.zeros(np.size(r))
    jtheta=-r*vphi
    jphi=r*vtheta

    return np.dstack((jr,jtheta,jphi))[0]



def specificAngularMomentum(pos,vel,coordinates='cartesian'):
    """
    PURPOSE : compute the value of specific angular momentum in gadget units
    INPUTS : pos = cartesian coordinates in gadget format (from readsnap)
             vel = cartesian velocity (must be same dimension than pos)
             coordinates = which coordinates systema are you using ?
    """

    options={'cartesian':specificAngularMomentum_cartesian,
                 'cylindrical':specificAngularMomentum_cylindrical,
                 'spherical':specificAngularMomentum_spherical
                 }

    try:
        return options[coordinates](pos,vel)
    except KeyError: #if wrong coordinates system, quit
        sys.exit()





def angularMomentum(pos,vel,mass,coordinates='cartesian'):
    """
    PURPOSE : compute the value of angular momentum in gadget units
    INPUTS : pos = cartesian coordinates in gadget format (from readsnap)
             vel = cartesian velocity (must be same dimension than pos)
             mass = mass of particles
             coordinates = which coordinates systema are you using ?
    """
    
    
    return mass[:,None]*specificAngularMomentum(pos,vel,coordinates=coordinates)


### TEMPERATURE
def meanMolecularWeight(Xh=0.76,ne=None):
    """
    PURPOSE: compute mean molecular weight
    INPUTS:  Xh = hydrogen fraction
             Ne = electron abundance from gadget output
    """

    Yh=(1-Xh)/(4*Xh) #helium fraction
    
    if ne is None: #adiabatic case
        mu=(1.+4 *Yh) / (1.+3.*Yh+ 1)
    else: #radiative cooling case
        mu = (1+4*Yh)/(1+Yh+ne)

    return mu


def temperature(u,mu):
    """
    PURPOSE : convert internal energy per unit mass in cgs to temperature in K
    INPUTS : u = specific internal energy in cgs
             mu = mean molecular weight (must be same dimension than u)
             ne = electron abundance
    OUTPUTS : temp = temperature in K
    """
    from constants import *

    u2temp=mu*PROTON_MASS*(ADIABATIC_INDEX-1)/BOLTZMANN_CONSTANT #total factor
    return u2temp*u

