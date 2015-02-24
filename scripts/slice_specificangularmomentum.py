###NAME: slice_density.py
###PURPOSE: plot a slice of density of the gas
###COMMENTS: does not work yet


import yt
import matplotlib.pyplot as plt
import numpy as np
from readgadget import *
import pdb




snap="/home/ldcao/Documents/GIZMO/run/L005_256_2/output/snapshot_000" #snapshot name
bbox=[[-3,3],[-3,3],[-3,3]] #boundary of your simulation
ds=yt.load(snap+".hdf5", unit_base={'length':('kpc',1.0)}, bounding_box=bbox) #add .hdf5 if needed


#find max density peak
ad=ds.all_data()
density = ad[("PartType0","density")]
wdens = np.where(density == np.max(density))
coordinates = ad[("PartType0","Coordinates")]
center = coordinates[wdens][0]
print 'center = ',center


field='PartType0_smoothed_particle_specific_angular_momentum_z'
slc=yt.SlicePlot(ds,'z',field) #define axis and center on densest cell
#slc.set_zlim(field,-5,5) #change colorbar range

#slc.zoom(64) #do you want to zoom in ?                                                            

slc.save() #save to png file
