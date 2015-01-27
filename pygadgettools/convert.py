### NAME: convert.py
### PURPOSE: convert position, velocity, and energy to other coordinate systems or units


import numpy as np



### i should use a wrapper convert.cartesian2spherical(pos,'pos')
##oh lala


## POSITION
def position_cartesian2spherical(pos,center=[0,0,0]):
    '''
    PURPOSE : convert POS cartesian into spherical coordinates
    INPUTS : pos = position in cartesian coordinates in Gadget format
             center = center of the new coordinate system in cartesian
    OUTPUTS: newpos = position in spherical coordinates in Gadget format
    '''

    #shift center
    pos-=center

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




def cartesian2cylindrical(pos,center=[0,0,0]):
    '''
    PURPOSE : convert POS cartesian into cylindrical coordinates
    INPUTS : pos = position in cartesian coordinates in Gadget format
             center = center of the new coordinate system in cartesian
    '''
    
    #shift center
    pos-=center
    

    #save cartesian position of each particle
    x=pos[:,0]
    y=pos[:,1]
    z=pos[:,2]

    r= np.sqrt(x**2+y**2)
    theta=np.arctan2(y,x)


    return np.dstack((r,theta,z))[0]



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



## for other transformation see : http://www.geom.uiuc.edu/docs/reference/CRC-formulas/node42.html

## VELOCITY



## ENERGY
