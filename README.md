# pygadgettools
Python toolbox for basic analysis of GADGET data. 

Author : Long Do Cao

Date of creation : 27th January 2015








## REQUIREMENTS
* numpy



### pygadgettools
Package providing basic analysis for gadget data


### scripts
This directory contains some simple script to generate some 2D plots using YT, adapted to Gadget-2.


## HOW TO USE

First, you can gain access to the functions by putting at the top of your script:

```python
import pygadgettools as gt
```

Then, the following functions are available directly :


```python
gt.analysis                   gt.mean_molecular_weight
gt.angular_momentum           gt.names
gt.change_coordinates         gt.physics
gt.convert                    gt.profile
gt.create_grid                gt.specific_angular_momentum
gt.filter                     gt.temperature
gt.geometry                   gt.units
gt.get_full_path 
```

You can get the description of each function by calling the help() command :

```python
help(gt.profile)
```

For example, let's say you want to compute the density profile along the z at points you want to define, you could do the following:


```python
from pygadgetreader import *
import pygadgettools as gt
import numpy as np
import matplotlib.pyplot as plt

## read the data
pos=readsnap("snapshot_000","pos","gas")
rho=readsnap("snapshot_000","rho","gas")
z=pos[:,2] #extract only the z-coordinates

##create the profile along which you want the profile
axis=np.linspace(0,1,100) #create an axis [0,1] with 100 points
profile=gt.profile.mean(z,rho,axis) #compute the profile as the mean of each shell

##make a figure
plt.figure()
plt.plot(axis,profile)
plt.show()
```

