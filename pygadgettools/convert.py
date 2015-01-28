### NAME: convert.py
### PURPOSE: convert position, velocity, and energy to other coordinate systems or units


import numpy as np



### i should use a wrapper convert.cartesian2spherical(pos,'pos')



## POSITION
def position_cartesian2spherical(pos):
    '''
    PURPOSE : convert POS cartesian into spherical coordinates
    INPUTS : pos = position in cartesian coordinates in Gadget format
             center = center of the new coordinate system in cartesian
    OUTPUTS: newpos = position in spherical coordinates in Gadget format
    '''

    #save cartesian position of each particle
    x=pos[:,0]
    y=pos[:,1]
    z=pos[:,2]

    r=np.sqrt(x**2+y**2+z**2) #radius position of each particle

    #define theta and take care of r=0 case
    theta=np.zeros(np.size(x))
    ind_zero=np.where(r == 0.) #is there any point where radius is 0 ?
    ind_nozero=np.where(r !=0) 
    if np.size(ind_zero) == 0:
        theta=np.arccos(z/r)        
    else:
        theta[ind_nozero]= np.arccos(z[ind_nozero]/r[ind_nozero])        
        theta[ind_zero]=0.

    phi=np.arctan2(y,x)

    return np.dstack((r,theta,phi))[0]




def position_cartesian2cylindrical(pos):
    '''
    PURPOSE : convert POS cartesian into cylindrical coordinates
    INPUTS : pos = position in cartesian coordinates in Gadget format
             center = center of the new coordinate system in cartesian
    '''
    
    #save cartesian position of each particle
    x=pos[:,0]
    y=pos[:,1]
    z=pos[:,2]

    rho= np.sqrt(x**2+y**2)
    theta=np.arctan2(y,x)


    return np.dstack((rho,theta,z))[0]



def position_spherical2cartesian(pos):
    """
    PURPOSE: convert spherical to cartesian coordinates
    INPUTS: pos = [r,theta,phi]
    COMMENTS: * center is not supported yet
    """

    r=pos[:,0]
    theta=pos[:,1]
    phi=pos[:,2]

    x=r*np.sin(theta)*np.cos(phi)
    y=r*np.sin(theta)*np.sin(phi)
    z=r*np.cos(theta)

    return np.dstack((x,y,z))[0]


def position_spherical2cylindrical(pos):
    """
    PURPOSE: convert position spherical to cylindrical coordinates
    INPUTS: pos = [r,theta,phi]
    """

    r=pos[:,0]
    theta_spherical=pos[:,1]
    phi_spherical=pos[:,2]

    rho=r*np.sin(theta_spherical)
    theta_cylindrical=phi_spherical
    z=r*np.cos(theta_spherical)

    return np.dstack((rho,theta_cylindrical,z))[0]


def position_cylindrical2cartesian(pos):
    """
    PURPOSE: convert cylindrical to cartesian coordinates
    INPUTS: pos = [rho,theta,z]
    COMMENTS: * center is not supported yet
    """

    rrho=pos[:,0]
    theta=pos[:,1]
    z=pos[:,2]

    x=rho*np.cos(theta)
    y=rho*np.sin(theta)
    z=z

    return np.dstack((x,y,z))[0]


def position_cylindrical2spherical(pos):
    """
    PURPOSE: convert cylindrical to spherical coordinates
    INPUTS: pos = [r,theta,z]
    COMMENTS: * center is not supported yet
    """

    rho=pos[:,0]
    theta_cylindrical=pos[:,1]
    z=pos[:,2]

    r=np.sqrt(rho**2+z**2)
    theta_spherical=np.arctan2(rho,z)
    phi=theta_cylindrical

    return np.dstack((r,theta_spherical,phi))[0]





## VELOCITY
def velocity_cartesian2cylindrical(pos,vel):
    '''
    PURPOSE : convert VEL cartesian into cylindrical coordinates
    INPUTS : pos = position in cartesian coordinates in Gadget format
             vel = velocity in cartesian coordinates
    '''
    
    #save cartesian position of each particle
    x=pos[:,0]
    y=pos[:,1]
    z=pos[:,2]

    #save cartesian velocities
    vx=vel[:,0]
    vy=vel[:,1]
    vz=vel[:,2]

    #convert to cylindrical coordinates
    r,theta,z=position_cartesian2cylindrical(pos)

    #compute cylindrical velocities
    vr=vx*np.cos(theta) + vy*np.sin(theta)
    vtheta=-vx*np.sin(theta) + vy*np.cos(theta)
    vz=vz
    

    return np.dstack((vr,vtheta,vz))[0]







def velocity_cartesian2spherical(pos,vel):
    '''
    PURPOSE : convert VEL cartesian into spherical coordinates
    INPUTS : pos = position in cartesian coordinates in Gadget format
             vel = velocity in cartesian coordinates
    '''
    
    #save cartesian position of each particle
    x=pos[:,0]
    y=pos[:,1]
    z=pos[:,2]

    #save cartesian velocities
    vx=vel[:,0]
    vy=vel[:,1]
    vz=vel[:,2]

    #convert to spherical coordinates
    r,theta,phi=position.cartesian2spherical(pos)


    #compute spherical velocities
    vr = 1./r * (x*vx+y*vy+z*vz)
    vtheta = -1/np.sqrt(1.-(z/r)**2)* (vz + z/r**2*(x*vx+y*vy+z*vz))
    vphi= r*np.sin(theta)/(x**2+y**2) * (x*vy - y*vx)

    return np.dstack((vr,vtheta,vphi))[0]


def velocity_cylindrical2cartesian(pos,vel):
    '''
    PURPOSE : convert VEL cartesian into spherical coordinates
    INPUTS : pos = position in cylindrical coordinates similar to Gadget format
             vel = velocity in cylindrical coordinates similar to Gadget format
    '''
    
    #save cartesian position of each particle
    r=pos[:,0]
    theta=pos[:,1]
    z=pos[:,2]

    #save cyindrical velocities
    vr=vel[:,0]
    vtheta=vel[:,1]
    vz=vel[:,2]

    #compute cartesian velocities
    vx = vr*np.cos(theta) - vtheta*np.sin(theta)
    vy = vr*np.sin(theta) + vtheta*np.cos(theta)
    vz = vz

    return np.dstack((vx,vy,vz))[0]



## ENERGY
