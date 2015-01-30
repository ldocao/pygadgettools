###NAME: selectParticles.py
###PURPOSE: select particles with some filter


import numpy as np
import changeCoordinates
import pdb




### GEOMETRY

def insideSphere(pos,rselect,center=[0,0,0]):
    """
    PURPOSE: return a filter (boolean) to select all particles inside the sphere(center,r)
    INPUTS: POS = cartesian coordinates
            rselect = radius of sphere in same units than POS
            center = center of sphere in same units than POS in cartesian
    OUTPUTS: return boolean array
    """

    temp_pos=pos-center
    pos_sph=changeCoordinates.position_cartesian2spherical(temp_pos)
    r=pos_sph[:,0]
    return r<=rselect
    

def sphericalShell(pos,rmin,rmax,center=[0,0,0]):
    """
    PURPOSE: return a filter (boolean) to select all particles inside a spherical shell between rmin and rmax.
    INPUTS: POS = cartesian coordinates
            rmin = minimal radius of spherical shell
            rmin = maximal radius of spherical shell
            center = center of sphere in same units than POS in cartesian
    OUTPUTS: return index of particles 
    """

    temp_pos=pos-center
    pos_sph=changeCoordinates.position_cartesian2spherical(temp_pos)
    r=pos_sph[:,0]
    return ((r>=rmin) & (r<=rmax))


