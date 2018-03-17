


import numpy as np
from math import pi, log10, sqrt, pow


#find distance between three points
def distanceTo(tx, rx):
    return round(sqrt((tx[0]-rx[0])**2 + (tx[1]-rx[1])**2 + (tx[2]-rx[2])**2),2)

#find receiver path from one point to another
def receiverPathTrace(initialLocation, finalLocation):
    #define varing coordinates
    x = initialLocation[0]
    y = initialLocation[1]
    z = initialLocation[2]
    coordinateList = [[x, y, z]]
    #1. hamming distance
    xdiff = finalLocation[0] - initialLocation[0]
    ydiff = finalLocation[1] - initialLocation[1]
    zdiff = finalLocation[2] - initialLocation[2]
    #2. calculating distance
    distance = round(distanceTo(initialLocation, finalLocation))
    if distance == 0:       #when receiver remain on same locatioi.e. receiver does not move
        distance=1
    #3. find each incremental steps
    xstep = xdiff/distance
    ystep = ydiff/distance
    zstep = zdiff/distance
    #4. add steps to initial coordinates
    for i in range(distance):
        x = x + xstep
        y = y + ystep
        z = z + zstep
        #rounding numbers to nearest whole number for easy calculation
        tmpList = [round(x), round(y), round(z)]  
        coordinateList.append(tmpList)
    result = np.array(coordinateList)
    return result

#calculate Normalized Received Power
def normalizedPower(transmitterAntennaGain, receiverAntennaGain, wavelength):
    return transmitterAntennaGain*receiverAntennaGain* pow((wavelength/(4*pi)),2)

#calculate distance between transmitter and each location of receiver
def distanceList(receiverPath, transmitterLocation):
    resultDistance = []
    for i in range(len(receiverPath)):
        tmpDistance = (round(distanceTo(transmitterLocation, receiverPath[i]), 2))
        resultDistance.append(tmpDistance)
    return resultDistance

#calculate received power in 'dBm'
def receivedPower(nPower, distanceLos):
    rPowerList = []
    for i in distanceLos:
        rPowerList.append(round(10*log10(nPower) -20*log10(i), 4))
    return rPowerList
    

    

    
    
    
    
    