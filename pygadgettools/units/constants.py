### NAME: constants.py
### PURPOSE: define constants variables in cgs units.

import numpy as np

## Universal constants
PARSEC                 = 3.08567758e18 #in cm
SOLAR_MASS             = 1.9891e33
BOLTZMANN_CONSTANT     = 1.380658e-16
PROTON_MASS            = 1.6726231e-24
GRAVITATIONAL_CONSTANT = 6.67259e-8 
ADIABATIC_INDEX        = 5./3.
SECONDS_IN_YEAR        = 3600.*24.*365.25
ASTRONOMICAL_UNIT      = 1.49597871e13 #in cm


## Gadget Units
UnitLength   = PARSEC #             Kpc --> cm
UnitMass     = 1.989e43    # M_solar * 10^10 --> grams
UnitVelocity = 1.0e5       #            km/s --> cm/s
UnitTime     = UnitLength/UnitVelocity #Seconds
UnitEnergy   = UnitMass * UnitLength * UnitLength / (UnitTime*UnitTime) #Erg

