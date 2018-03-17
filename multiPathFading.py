
import numpy as np
from math import pi

def expressionLos(distanceLos, wavelength):
    expL = np.divide(np.exp(np.multiply(-1j*2*pi*wavelength,distanceLos)),distanceLos)
    return expL

def expressionFor(reflectionCoefficient, wavelength, rxAndTxDistance, anyKey):
    expFor = [0]*len(rxAndTxDistance[anyKey])
    for key in rxAndTxDistance.keys():
        val = rxAndTxDistance[key]
        tmpexpFor = np.multiply(reflectionCoefficient, np.divide(np.exp(np.multiply(-1j*2*pi*wavelength,val)),val))
        expFor = np.add(expFor, tmpexpFor)
    return expFor

def expressionSor(reflectionCoefficient, wavelength, rxAndTxDistanceSor):
    expSor = expressionFor(reflectionCoefficient, wavelength, rxAndTxDistanceSor, 'eastwest')
    return expSor






