

from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
ax = plt.axes(projection='3d')
import numpy as np
from imageLocation import imageLocationFor


def graphPlot(distanceLos, orderOfFadig, receivedPowerLosDb=0, receivedPowerForDb=0, receivedPowerSorDb=0):
    if orderOfFadig == 'los':
        #plt.subplot(221)
        plt.semilogx(distanceLos, receivedPowerLosDb)
        #plt.axis([1,50,-60,-30])
        plt.title('Line of Sight')
        
    if orderOfFadig == 'first':
        #plt.subplot(222)
        plt.semilogx(distanceLos, receivedPowerLosDb)
        plt.semilogx(distanceLos, receivedPowerForDb)
        #plt.axis([1,50,-60,-30])
        plt.title('First Order Reflection')
        
    if orderOfFadig == 'second':
        #plt.subplot(223)
        plt.semilogx(distanceLos, receivedPowerLosDb)
        plt.semilogx(distanceLos, receivedPowerForDb)
        plt.semilogx(distanceLos, receivedPowerSorDb)
        #plt.axis([1,50,-60,-30])
        plt.title('Second Order Reflection')

#draw a cube from its boundary coordinates
def cubePlot(boundaryCoordinates):
    for coord1 in boundaryCoordinates:
        for coord2 in boundaryCoordinates:
            bitChangeCount = 0
            for i in range(len(coord2)):
                if abs(coord2[i]-coord1[i]) == 0:
                    bitChangeCount+=1
            if bitChangeCount == 2:
                tmpCoord = np.array([coord1, coord2])
                plotLine(tmpCoord, 'black')  
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')         
      
def plotLine(coordArray, colour):
    tmpx = coordArray[0:len(coordArray),0]
    tmpy = coordArray[0:len(coordArray),1]
    tmpz = coordArray[0:len(coordArray),2]
    ax.plot3D(tmpx, tmpy, tmpz, colour)

def receiverPathPlot(receiverPath, transmitterLocation):
    x = receiverPath[0:len(receiverPath),0]
    y = receiverPath[0:len(receiverPath),1]
    z = receiverPath[0:len(receiverPath),2]
    ax.plot3D(x, y, z, 'red')
    ax.scatter3D(x, y, z)
    tx = [transmitterLocation[0]]
    ty = [transmitterLocation[1]]
    tz = [transmitterLocation[2]]
    ax.scatter3D(tx, ty, tz)

def planeLinePoint(receiver, image, planeCoefficient):
    #step1: find line vector
    p = np.array(receiver) # p(x1,y1,z1)
    q = np.array(image) #q(x2,y2,z2)
    pq = q-p    #pq(a,b,c)
    #print(pq)
    #step2: find t
    t = -1*(planeCoefficient[0]*p[0] + planeCoefficient[1]*p[1] + planeCoefficient[2]*p[2] + planeCoefficient[3]) / (planeCoefficient[0]*pq[0] + planeCoefficient[1]*pq[1] + planeCoefficient[2]*pq[2])
    #print(t)
    #step3: find point of intersection of the plane and line joining receiver and transmitter image on that plane
    reflectionPointFor = [round(p[0]+t*pq[0]), round(p[1]+t*pq[1]), round(p[2]+t*pq[2])]
    return reflectionPointFor
    
#planeLinePoint(receiver, image, planeCoefficient)
def reflectionPlotFor(planeCofficientDisctionary, receiverPath, transmitterLocation):
    colour = ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan']
    colourIndex = 0
    for key in planeCofficientDisctionary.keys():
        val = np.array(planeCofficientDisctionary[key])
        transmitterImage = imageLocationFor(transmitterLocation, val)
        #print(transmitterImage)
        for receiverPoint in receiverPath:
            #print(receiverPoint)
            reflectionPointFor = planeLinePoint(receiverPoint, transmitterImage, val)
            #print(reflectionPointFor)
            tmpArray = np.array([transmitterLocation, reflectionPointFor, receiverPoint])
            plotLine(tmpArray,colour[colourIndex])
        colourIndex+=1
        