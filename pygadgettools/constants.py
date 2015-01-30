### NAME: constants.py
### PURPOSE: define constants variables in cgs units.

import numpy as np

## Universal constants
PARSEC                 = 3.08567758e18 #in cm
SOLAR_MASS             = 1.9891e33
BOLTZMANN_CONSTANT     = 1.380658e-16
PROTON_MASS            = 1.6726231e-24;  
GRAVITATIONAL_CONSTANT = 6.67259e-8 



## Gadget Units
UnitLength   = 3.085678e18; #             Kpc --> cm
UnitMass     = 1.989e43;    # M_solar * 10^10 --> grams
UnitVelocity = 1.0e5;       #            km/s --> cm/s
UnitTime     = UnitLength/UnitVelocity; #Seconds
UnitEnergy   = UnitMass * UnitLength * UnitLength / (UnitTime*UnitTime); #Erg

