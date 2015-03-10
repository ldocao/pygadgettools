### NAME: convert.py
### PURPOSE: convert units from Gadget Units (GU) to cgs

import numpy as np
from .constants import *


def length(l):
    return l*UnitLength

def mass(m):
    return m*UnitMass

def velocity(v):
    return v*UnitVelocity

def time(t):
    return t*UnitTime

def energy(e):
    return e*UnitEnergy

def density(rho):
    return rho*UnitMass/UnitLength**3

def surfacedensity(rho):
    return rho*UnitMass/UnitLength**2

def energypermass(u):
    return u*UnitEnergy/UnitMass

def angular_momentum(l):
    return l*UnitLength*UnitMass*UnitVelocity

def specificangular_momentum(l):
    return l*UnitLength*UnitVelocity

def accretion_rate(l):
    return l*UnitMass/UnitTime
