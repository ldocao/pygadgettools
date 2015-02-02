###NAME: slice_densityDM.py
###PURPOSE: plot a slice of density of the dark matter

import yt
import matplotlib.pyplot as plt
import numpy as np
from readgadget import *
import pdb




snap="/home/ldcao/Documents/GIZMO/run/L005_1/output/snapshot_000" #snapshot name
bbox=[[-3,3],[-3,3],[-3,3]] #boundary of your simulation
ds=yt.load(snap+".hdf5", unit_base={'length':('kpc',1.0)}, bounding_box=bbox) #add .hdf5 if needed

slc=yt.SlicePlot(ds,'z',("deposit","PartType1_cic")) #define axis
slc.annotate_quiver(("deposit","all_cic_velocity_x"),("deposit","all_cic_velocity_y"),factor=16) #add velocity arrows

#slc.zoom(4) #do you want to zoom in ?                                                              #slc.set_zlim('PartType1_cic',3e-30,1e-28) #change colorbar range
slc.save() #save to png file

