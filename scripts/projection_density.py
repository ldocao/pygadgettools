###NAME: projection_density.py
###PURPOSE: plot a projection of density of the gas

import yt
import matplotlib.pyplot as plt
import numpy as np
from readgadget import *
import pdb




snap="/home/ldcao/Documents/GIZMO/run/L005_256_2s5/output/snapshot_079" #snapshot name
bbox=[[-3100,3100],[-3100,3100],[-3100,3100]] #boundary of your simulation
ds=yt.load(snap+".hdf5", unit_base={'length':('pc',1.0)}, bounding_box=bbox) #add .hdf5 if needed


#find max density peak
ad=ds.all_data()
density = ad[("PartType0","density")]
wdens = np.where(density == np.max(density))
coordinates = ad[("PartType0","Coordinates")]
center = coordinates[wdens][0]
print 'center = ',center


prj=yt.ProjectionPlot(ds,'z',"PartType0_smoothed_density",center=center,weight_field="PartType0_smoothed_density") #define axis and center on densest cell
prj.annotate_quiver(("deposit","PartType0_cic_velocity_x"),("deposit","PartType0_cic_velocity_y"))

#prj.zoom(64) #do you want to zoom in ?                                          
prj.save() #save to png file

