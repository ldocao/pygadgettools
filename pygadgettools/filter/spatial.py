###NAME: spatial.py
###PURPOSE: select particles with spatial filter


import numpy as np
from geometry.coordinates import change_coordinates



def sphere(pos,rselect,center=[0,0,0]):
    """ Return a filter (boolean) to select all particles inside the sphere(center,r)

    Parameters:
    ----------

    pos : float array
         cartesian coordinates

    rselect : float
         radius of sphere in same units than pos

    center : list or float array (3)
         center of sphere in cartesian coordinates and same units than pos

    """

    r=change_coordinates(pos-center,"pos","cart","sph")[:,0]
    return r<=rselect
    

def spherical_shell(pos,rmin,rmax,center=[0,0,0]):
    """Return a filter (boolean) to select all particles inside a spherical shell between rmin and rmax.

    Parameters:
    ----------

    pos : float array
         cartesian coordinates

    rmin : float
         minimal radius of spherical shell

    rmax : float
         maximal radius of spherical shell

    center : list or float array (3)
         center of sphere in cartesian coordinates and same units than pos
    """

    r=change_coordinates(pos-center,"pos","cart","sph")[:,0]
    return ((r>=rmin) & (r<=rmax))


