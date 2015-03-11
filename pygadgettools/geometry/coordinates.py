### NAME: coordinates.py
### PURPOSE: convert position, velocity, and energy to other coordinate systems or units


import numpy as np
import warnings
import sys
from internals.sanity_check import \
    _check_if_keyword_is_correct, _check_dimension



def change_coordinates(pos,variable_type,sys1,sys2,*args):
    """Change the coordinates system of a variable

    Parameters:
    ----------

    pos : float array [N,3]
        position of particles

    variable_type : string
        type of the variable to convert (eg.: pos, vel, etc.)

    sys1 : string
        the initial coordinate system of the variables you are passing in. All variables MUST be in the same coordinate system. Currently available : ('cart', 'cyl', 'sph') for (cartesian, cylindrical, spherical) respectively.

    sys2 : string
        the final coordinate system you want your variables to be in. Currently available : ('cart', 'cyl', 'sph') for (cartesian, cylindrical, spherical) respectively. sys2 must be different than sys1.

    *args : float array [N,3]
        other variables useful for conversion. For example, if you want to convert velocity, you may provide it here as an additional argument.


    Examples:
    --------
    
    >>> POS=np.array([[1,1,0]])
    >>> change_coordinates(POS,"pos","cart","sph")
    array([[ 1.41421356,  1.57079633,  0.78539816]])

    >>> POS=np.array([[1,np.pi,1]])
    >>> VEL=np.array([[1,1,1]])
    >>> change_coordinates(POS,"vel","cyl","cart",VEL)
    array([[-1., -1.,  1.]])
    
    """

        
    ## some sanity check
    list_sys=["cart","cyl","sph"] #list of authorized strings for sys1 and sys2. I could also authorize complete names
    list_var=["pos","vel"] #list of authorized strings for variable_type
    
    _check_if_keyword_is_correct(sys1,list_sys)
    _check_if_keyword_is_correct(sys2,list_sys)
    _check_if_keyword_is_correct(variable_type,list_var)
    ##should implement here a sanity check for pos dimension


    ## select the good function to call
    case="".join([sys1,sys2])    
    if variable_type == "pos":
        options={'cartcyl':_position_cartesian2cylindrical,
                 'cartsph':_position_cartesian2spherical,
                 'cylcart':_position_cylindrical2cartesian,
                 'cylsph':_position_cylindrical2spherical,
                 'sphcart':_position_spherical2cartesian,
                 'sphcyl':_position_spherical2cylindrical
                    }
        output=options[case](pos)
    elif variable_type == "vel":
        options={'cartcyl':_velocity_cartesian2cylindrical,
                 'cartsph':_velocity_cartesian2spherical,
                 'cylcart':_velocity_cylindrical2cartesian,
                 'cylsph':_velocity_cylindrical2spherical,
                 'sphcart':_velocity_spherical2cartesian,
                 'sphcyl':_velocity_spherical2cylindrical
                    }
        output=options[case](pos,*args)
    else: #should never go here if the sanity check above is properly done
        sys.exit()
    
    return output














## POSITION
def _position_cartesian2spherical(pos):
    """Convert POS cartesian into spherical coordinates

    Parameters:
    ----------
    pos : float array (N,3)
        position in cartesian coordinates in Gadget format
    """

    #save cartesian position of each particle
    x=pos[:,0]
    y=pos[:,1]
    z=pos[:,2]

    r=np.sqrt(x**2+y**2+z**2) #radius position of each particle

    #define theta and take care of r=0 case
    theta=np.zeros(np.size(x))
    ind_zero=(r == 0.) #is there any point where radius is 0 ?
    theta= np.arccos(z/r)        
    theta[ind_zero]=0.

    phi=np.arctan2(y,x)

    return np.dstack((r,theta,phi))[0]




def _position_cartesian2cylindrical(pos):
    """Convert POS cartesian into cylindrical coordinates

    Parameters:
    ----------
    pos : float array (N,3)
        position in cartesian coordinates in Gadget format
    """

    
    #save cartesian position of each particle
    x=pos[:,0]
    y=pos[:,1]
    z=pos[:,2]

    rho= np.sqrt(x**2+y**2)
    theta=np.arctan2(y,x)


    return np.dstack((rho,theta,z))[0]



def _position_spherical2cartesian(pos):
    """Convert POS spherical into cartesian coordinates

    Parameters:
    ----------
    pos : float array (N,3)
        position in spherical coordinates in Gadget format
    """
    
    r=pos[:,0]
    theta=pos[:,1]
    phi=pos[:,2]

    if any(theta>np.pi) or any(theta<0): #sanity check. not necessary for phi.
        raise ValueError, "Theta beyond [0,pi]. Exiting."


    x=r*np.sin(theta)*np.cos(phi)
    y=r*np.sin(theta)*np.sin(phi)
    z=r*np.cos(theta)

    return np.dstack((x,y,z))[0]


def _position_spherical2cylindrical(pos):
    """Convert POS spherical into cylindrical coordinates

    Parameters:
    ----------
    pos : float array (N,3)
        position in spherical coordinates in Gadget format
    """
    

    r=pos[:,0]
    theta_spherical=pos[:,1]
    phi_spherical=pos[:,2]

    if any(theta_spherical>np.pi) or any(theta_spherical<0): #sanity check. not necessary for phi.
        raise ValueError, "Theta beyond [0,pi]. Exiting."

    rho=r*np.sin(theta_spherical)
    theta_cylindrical=phi_spherical
    z=r*np.cos(theta_spherical)

    return np.dstack((rho,theta_cylindrical,z))[0]


def _position_cylindrical2cartesian(pos):
    """Convert POS cylindrical into cartesian coordinates

    Parameters:
    ----------
    pos : float array (N,3)
        position in cylindrical coordinates in Gadget format
    """
    
    rho=pos[:,0]
    theta=pos[:,1]
    z=pos[:,2]

    x=rho*np.cos(theta)
    y=rho*np.sin(theta)
    z=z

    return np.dstack((x,y,z))[0]


def _position_cylindrical2spherical(pos):
    """Convert POS cylindrical into spherical coordinates

    Parameters:
    ----------
    pos : float array (N,3)
        position in cylindrical coordinates in Gadget format
    """

    rho=pos[:,0]
    theta_cylindrical=pos[:,1]
    z=pos[:,2]

    r=np.sqrt(rho**2+z**2)
    theta_spherical=np.arctan2(rho,z)
    phi=theta_cylindrical

    return np.dstack((r,theta_spherical,phi))[0]





## VELOCITY
def _velocity_cartesian2cylindrical(pos,vel):
    """Convert velocity from cartesian to cylindrical coordinates

    Parameters:
    ----------
    pos : float array (N,3)
        position in cartesian coordinates

    vel : float array (N,3)
        velocity in cartesian coordinates
    """
    
    
    
    #save cartesian velocities
    vx=vel[:,0]
    vy=vel[:,1]
    vz=vel[:,2]

    #convert to cylindrical coordinates
    pos_cyl=_position_cartesian2cylindrical(pos) #cylindrical coordinates
    theta=pos_cyl[:,1]

    #compute cylindrical velocities
    vr=vx*np.cos(theta) + vy*np.sin(theta)
    vtheta=-vx*np.sin(theta) + vy*np.cos(theta)
    vz=vz
    

    return np.dstack((vr,vtheta,vz))[0]





def _velocity_cartesian2spherical(pos,vel):
    """Convert velocity from cartesian to spherical coordinates

    Parameters:
    ----------
    pos : float array (N,3)
        position in cartesian coordinates

    vel : float array (N,3)
        velocity in cartesian coordinates
    """

    
    #save cartesian position of each particle
    x=pos[:,0]
    y=pos[:,1]
    z=pos[:,2]

    #save cartesian velocities
    vx=vel[:,0]
    vy=vel[:,1]
    vz=vel[:,2]

    #convert to spherical coordinates
    pos_sph=_position_cartesian2spherical(pos) #spherical coordinates
    r=pos_sph[:,0]
    theta=pos_sph[:,1]
    phi=pos_sph[:,2]


    #compute spherical velocities
    vr = vx*np.sin(theta)*np.cos(phi) + vy*np.sin(theta)*np.sin(phi) + vz*np.cos(theta)
    vtheta = vx*np.cos(theta)*np.cos(phi) + vy*np.cos(theta)*np.sin(phi) - vz*np.sin(theta)
    vphi = -vx*np.sin(phi) + vy*np.cos(phi)

    if np.sum(r==0)!=0: #if some points are at the origin
        warnings.warn("Spherical velocity is not defined at origin. Returning 0.")
        vr[r==0]=0
        vtheta[r==0]=0
        vphi[r==0]=0


    return np.dstack((vr,vtheta,vphi))[0]




def _velocity_cylindrical2cartesian(pos,vel):
    """Convert velocity from cylindrical to cartesian coordinates

    Parameters:
    ----------
    pos : float array (N,3)
        position in cylindrical coordinates

    vel : float array (N,3)
        velocity in cylindrical coordinates
    """
    
    
    #save cartesian position of each particle
    theta=pos[:,1]

    #save cyindrical velocities
    vr=vel[:,0]
    vtheta=vel[:,1]
    vz=vel[:,2]

    #compute cartesian velocities
    vx = vr*np.cos(theta) - vtheta*np.sin(theta)
    vy = vr*np.sin(theta) + vtheta*np.cos(theta)
    vz = vz

    return np.dstack((vx,vy,vz))[0]





def _velocity_cylindrical2spherical(pos,vel):
    """Convert velocity from cylindrical to spherical coordinates

    Parameters:
    ----------
    pos : float array (N,3)
        position in cylindrical coordinates

    vel : float array (N,3)
        velocity in cylindrical coordinates
    """
    
    pos_cart=_position_cylindrical2cartesian(pos)
    vel_cart=_velocity_cylindrical2cartesian(pos,vel)
    vel_sph=_velocity_cartesian2spherical(pos_cart,vel_cart)

    return vel_sph




def _velocity_spherical2cartesian(pos,vel):
    """Convert velocity from spherical to cartesian coordinates

    Parameters:
    ----------
    pos : float array (N,3)
        position in spherical coordinates

    vel : float array (N,3)
        velocity in spherical coordinates
    """
    
    #save cartesian position of each particle
    r=pos[:,0]
    theta=pos[:,1]
    phi=pos[:,2]


    #save cyindrical velocities
    vr=vel[:,0]
    vtheta=vel[:,1]
    vphi=vel[:,2]


    #compute cartesian velocities
    vx = vr*np.sin(theta)*np.cos(phi) + vtheta*np.cos(theta)*np.cos(phi) - vphi*np.sin(phi)
    vy = vr*np.sin(theta)*np.sin(phi) + vtheta*np.cos(theta)*np.sin(phi) + vphi*np.cos(phi)
    vz = vr*np.cos(theta) - vtheta*np.sin(theta)

    return np.dstack((vx,vy,vz))[0]



def _velocity_spherical2cylindrical(pos,vel):
    """Convert velocity from spherical to cylindrical coordinates

    Parameters:
    ----------
    pos : float array (N,3)
        position in spherical coordinates

    vel : float array (N,3)
        velocity in spherical coordinates
    """
    
    pos_cart=_position_spherical2cartesian(pos)
    vel_cart=_velocity_spherical2cartesian(pos,vel)
    vel_cyl=_velocity_cartesian2cylindrical(pos_cart,vel_cart)

    return vel_cyl



