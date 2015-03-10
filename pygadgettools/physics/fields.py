###NAME: fields.py
###PURPOSE: compute some interesting physical quantities

from common import *
import numpy as np




### ANGULAR MOMENTUM
def _specific_angular_momentum_cartesian(pos,vel):
    """Compute the specific angular momentum in cartesian coordinates


    Parameters:
    ----------

    pos : float array [N,3]
        cartesian coordinates in gadget format (from readsnap)

    vel : float array [N,3]
        cartesian velocity (must be same dimension than pos)
   
    """
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


def _specific_angular_momentum_cylindrical(pos,vel):
    """Compute the specific angular momentum in cylindrical coordinates


    Parameters:
    ----------

    pos : float array [N,3]
        cylindrical coordinates in gadget format (from readsnap)

    vel : float array [N,3]
        cyindrical velocity (must be same dimension than pos)
   
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


def _specific_angular_momentum_spherical(pos,vel):
    """Compute the specific angular momentum in spherical coordinates


    Parameters:
    ----------

    pos : float array [N,3]
        spherical coordinates in gadget format (from readsnap)

    vel : float array [N,3]
        spherical velocity (must be same dimension than pos)
   
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



def specific_angular_momentum(pos,vel,coordinates='cartesian'):
    """Compute the specific angular momentum in spherical coordinates


    Parameters:
    ----------

    pos : float array [N,3]
        spherical coordinates in gadget format (from readsnap)

    vel : float array [N,3]
        spherical velocity (must be same dimension than pos)

    coordinates : string
        which coordinates system are you using ? ('cartesian','cylindrical','spherical')
   
    """

    options={'cartesian':_specific_angular_momentum_cartesian,
             'cylindrical':_specific_angular_momentum_cylindrical,
             'spherical':_specific_angular_momentum_spherical
                 }

    try:
        return options[coordinates](pos,vel)
    except KeyError: #if wrong coordinates system, quit
        sys.exit()





def angular_momentum(pos,vel,mass,coordinates='cartesian'):
    """Compute the angular momentum in spherical coordinates


    Parameters:
    ----------

    pos : float array [N,3]
        spherical coordinates in gadget format (from readsnap)

    vel : float array [N,3]
        spherical velocity (must be same dimension than pos)

    mass : float array [N]
        mass of particles

    coordinates : string
        which coordinates system are you using ? ('cartesian','cylindrical','spherical')
   
    """
    
    return mass[:,None]*specificAngularMomentum(pos,vel,coordinates=coordinates)






### TEMPERATURE
def mean_molecular_weight(Xh=0.76,ne=None):
    """Compute mean molecular weight

    Parameters:
    ----------

    Xh : float array
        hydrogen fraction from gadget output (Nh)

    Ne : float array
        electron abundance from gadget utput

    """

    Yh=(1-Xh)/(4*Xh) #helium fraction
    
    if ne is None: #adiabatic case
        mu=(1.+4 *Yh) / (1.+3.*Yh+ 1)
    else: #radiative cooling case
        mu = (1+4*Yh)/(1+Yh+ne)

    return mu



def temperature(u,mu):
    """Convert internal energy per unit mass in cgs to temperature in K.

    Parameters:
    ----------

    u : float array
         specific internal energy in cgs

    mu :float array
         mean molecular weight (must be same dimension than u)

    ne : float array
         electron abundance

    """
    

    u2temp=mu*PROTON_MASS*(ADIABATIC_INDEX-1)/BOLTZMANN_CONSTANT #total factor
    return u2temp*u

