'''
Created on Dec 11, 2017

@author: ansari
'''

import numpy as np
import matplotlib.pyplot as plt
from math import pow
from computation import normalizedPower, receiverPathTrace, distanceList, receivedPower
from imageLocation import boundary, planeCoefficient, imageLocationFor, rxTxDistanceFor, imageLocationSor, boundaryCoordinates
from multiPathFading import expressionLos, expressionFor, expressionSor
from plot import graphPlot, cubePlot, receiverPathPlot, reflectionPlotFor
#from test import rxTxDistanceFor

#setting parameters
transmitterAntennaGain = 1.6
receiverAntennaGain = 1.6
frequency = pow(10,9)
signalSpeed = 3*pow(10,8)
reflectionCoefficient = -0.7
wavelength = signalSpeed/frequency
nPower = round(normalizedPower(transmitterAntennaGain, receiverAntennaGain, wavelength),4)

#defining Cube size, we want to form a cube emerge from origin to cube size in 3 dimension
cubeSize = int(input('Cube Size:'))
#cubeSize = 50

#form a cube of size(length) = cubeSize and find plane boundary coordinates and plane coefficient
boundaryDictionary = boundary(cubeSize) #compute boundaries of a plane and assign then to their respective plane
boundaryCoordinate = np.array(boundaryCoordinates(cubeSize))
#transmitter location 
#transmitterLocation = [25,13,35]
transmitterLocation = [int(x) for x in input("Transmitter Location:").split(',')]

#receiver location
#receiverLocationStart = [42,25,25]
#receiverLocationEnd = [42,25,25]
receiverLocationStart = [int(x) for x in input("Receiver Starting Point:").split(',')]
receiverLocationEnd = [int(x) for x in input("Receiver Ending Point:").split(',')]

#find receiver path from one point to another
receiverPath = np.array(receiverPathTrace(receiverLocationStart, receiverLocationEnd))
#print('receiverPath', receiverPath)

#find distance between each received path and transmitter
distanceLos = np.array(distanceList(receiverPath, transmitterLocation),int)
#print(distanceLos)

#we now want to find joint received power from LOS and FOR
#assign plane coefficient to their corresponding plane name 
planeCofficientDisctionary = {}
for i in boundaryDictionary.keys():
    planeCofficientDisctionary[i] = planeCoefficient(boundaryDictionary[i]) 

#compute first order reflection(FOR) possible images of transmitter
#imageLocationFor = imageLocationFor(transmitterLocation, planeCofficientDisctionary)
imageLocationDictionaryFor = {}
for key in planeCofficientDisctionary.keys():
    planeCofficient = planeCofficientDisctionary[key]
    image =  imageLocationFor(transmitterLocation, planeCofficient)
    #assign all image to corresponding plane
    imageLocationDictionaryFor[key] = image
#distance between Rx and Tx-image(FOR) location is equal to path made by Rx and Tx(FOR)
rxAndTxDistanceFor = rxTxDistanceFor(receiverPath, imageLocationDictionaryFor) 
#print(rxAndTxDistanceFor)

#first draw a cube and the receiver path and transmitter location
plt.figure(1)
receiverPathPlot(receiverPath, transmitterLocation)
cubePlot(boundaryCoordinate)
reflectionPlotFor(planeCofficientDisctionary, receiverPath, transmitterLocation)

#LOS received power at each movement of receiver
receivedPowerLosDb= np.array(receivedPower(nPower, distanceLos))
plt.figure(2)
plt.subplot(221)
graphPlot(distanceLos, 'los',receivedPowerLosDb)
#print('receivedPowerLosDb',receivedPowerLosDb) 

#combined Power Calculation (LOS + FOR)
#reflection coefficient value is -0.7 but there is no reflection for LOS. so we need to calculate them differently
expLos = expressionLos(distanceLos, wavelength) #LOS contribution alone
expFor = expressionFor(reflectionCoefficient, wavelength, rxAndTxDistanceFor, 'east')
expressionTotalFor = np.add(expLos, expFor)
receivedPowerFor = np.multiply(nPower, np.power(abs(expressionTotalFor),2))
receivedPowerForDb = np.multiply(10, np.log10(receivedPowerFor))
plt.figure(2)
plt.subplot(222)
graphPlot(distanceLos, 'first', receivedPowerLosDb, receivedPowerForDb)
#print('receivedPowerForDb', receivedPowerForDb)

#for second order  reflection (SOR)
#compute first order reflection(SOR) possible images of transmitter
imageLocationDictionarySor = imageLocationSor(imageLocationDictionaryFor, planeCofficientDisctionary)
#print(imageLocationDictionarySor)
#distance between Rx and Tx-image(SOR) location is equal to path made by Rx and Tx(FOR)
rxAndTxDistanceSor = rxTxDistanceFor(receiverPath, imageLocationDictionarySor) 
#print(rxAndTxDistanceSor)

#combined Power Calculation (LOS + FOR + SOR)
expSor = expressionSor(reflectionCoefficient, wavelength, rxAndTxDistanceSor)
expressionTotalSor = np.add(expressionTotalFor, expSor)
receivedPowerSor = np.multiply(nPower, np.power(abs(expressionTotalSor),2))
receivedPowerSorDb = np.multiply(10, np.log10(receivedPowerSor))
plt.figure(2)
plt.subplot(223)
graphPlot(distanceLos, 'second', receivedPowerLosDb, receivedPowerForDb, receivedPowerSorDb)
#print('receivedPowerSorDb', receivedPowerSorDb)
plt.show()
