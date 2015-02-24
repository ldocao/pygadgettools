###NAME: slice_velocity.py
###PURPOSE: plot a slice of the cylindrical velocity of the gas
###COMMENTS: does not work yet



import yt
import matplotlib.pyplot as plt
import numpy as np
from readgadget import *
import pdb




snap="/home/ldcao/Documents/GIZMO/run/L005_1/output/snapshot_000" #snapshot name
bbox=[[-3,3],[-3,3],[-3,3]] #boundary of your simulation
ds=yt.load(snap+".hdf5", unit_base={'length':('kpc',1.0)}, bounding_box=bbox) #add .hdf5 if needed


#find max density peak
ad=ds.all_data()
density = ad[("PartType0","density")]
wdens = np.where(density == np.max(density))
coordinates = ad[("PartType0","Coordinates")]
center = coordinates[wdens][0]
print 'center = ',center


## do ds.derived_field_list to see available fields
field='PartType0_smoothed_particle_cylindrical_velocity_theta'
slc=yt.SlicePlot(ds,'z',field) #define axis and center on densest cell
#slc.set_zlim(field,-5,5) #change colorbar range

#slc.zoom(64) #do you want to zoom in ?                                                            

slc.save() #save to png file

