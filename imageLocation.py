

from computation import distanceTo
import numpy as np
from fractions import gcd
#import math

def boundaryCoordinates(n):
    return [[0,0,0], [0,0,n], [0,n,0], [0,n,n], [n,0,0], [n,0,n], [n,n,0], [n,n,n]] #coordinates respectively in :O, E, A, F, C, D, B, G: 

#compute boundary and plane coefficient
def boundary(n):
    boundaryCoordinate = boundaryCoordinates(n)
    cubeside = 6
    east = []   #OABC
    west = []   #DEFG
    north = []  #OAFE
    south = []  #BCDG
    top = []    #ABGF
    bottom = [] #OCDE
    for i in range(cubeside-1):
        for j in boundaryCoordinate:
            if j[0] == 0 and len(north)<4 :
                north.append(j)
            if j[0] == n and len(south)<4 :
                south.append(j)
            if j[1] == 0 and len(bottom)<4 :
                bottom.append(j)
            if j[1] == n and len(top)<4 :
                top.append(j)
            if j[2] == 0 and len(east)<4 :
                east.append(j)
            if j[2] == n and len(west)<4 :
                west.append(j)           
    boundaryDictionary = {'east':east, 'west':west, 'north':north, 'south':south, 'top':top, 'bottom':bottom}
    return boundaryDictionary
    
#find coefficient of plane equation
def planeCoefficient(planeCoordinates):
    p = np.array(planeCoordinates[1])
    q = np.array(planeCoordinates[2])
    r = np.array(planeCoordinates[3])
    
    pq = q - p
    pr = r - p
    coefficient = np.cross(pq, pr) 
    constant = -np.dot(coefficient, p)
    tmpresult = np.append(coefficient, constant)
    A = tmpresult.tolist()
    res = A[0]
    for c in A[1::]:
        res = gcd(res , c)
    result = np.array(tmpresult)
    result = np.divide(result,res)
    return result.tolist() #convert array to list

'''  
#assign plane coefficient to their corresponding plane name 
boundaryDictionary = boundary(50)
boundaryDictionaryKeys = boundaryDictionary.keys()
planeCofficientDisctionary = {}
for i in boundaryDictionaryKeys:
    planeCofficientDisctionary[i] = planeCoefficient(boundaryDictionary[i]) 

#find perpendicular distance between Transmitter and the plane
perpendicularDistanceDisctionary = {}
for key in planeCofficientDisctionary.keys():
    val = planeCofficientDisctionary[key]
    perpendicularDistance = abs(val[0]*transmitterLocation[0] + val[1]*transmitterLocation[1] + val[2]*transmitterLocation[2] + val[3])/math.sqrt(val[0]**2+val[1]**2+val[2]**2)
    perpendicularDistanceDisctionary[key] = perpendicularDistance            
print(perpendicularDistanceDisctionary)
'''
'''
#compute first order reflection(FOR) possible images of transmitter
def imageLocationFor(transmitterLocation, receiverPath, planeCofficientDisctionary):
    imageLocationDictionary = {}
    for key in planeCofficientDisctionary.keys():
        val = planeCofficientDisctionary[key]
        for trElement in transmitterLocation:
            
'''

#compute first order reflection(FOR) possible images of transmitter
def imageLocationFor(transmitterLocation, planeCofficient):
    #imageLocationDictionary = {}
    #for key in planeCofficientDisctionary.keys():
    val = planeCofficient
    #define  L=(transmitterLocation) + t* (each plane coefficient and solve t as below
    t = -1*(val[0]*transmitterLocation[0] + val[1]*transmitterLocation[1] + val[2]*transmitterLocation[2] + val[3]) / (val[0]**2 + val[1]**2 + val[2]**2)
    #find perpendicular point on plane from transmitterLocation
    midPoint = [transmitterLocation[0]+(val[0]*t), transmitterLocation[1]+(val[1]*t), transmitterLocation[2]+(val[2]*t)]
    #find image location using mid-point formula
    image = [round((2*midPoint[0])-transmitterLocation[0],2), round((2*midPoint[1])-transmitterLocation[1],2), round((2*midPoint[2])-transmitterLocation[2],2)]
    #assign all image to corresponding plane
    #imageLocationDictionary[key] = image
    return image

#compute second order reflection(SOR) possible images of transmitter
def imageLocationSor(imageLocationDictionary, planeCofficientDisctionary):
    imageLocationSorDisctionary = {}
    for imageKey in imageLocationDictionary.keys():
        for planeKey in planeCofficientDisctionary.keys():
            if imageKey!=planeKey:
                planeCofficient = planeCofficientDisctionary[planeKey]
                image =  imageLocationFor(imageLocationDictionary[imageKey], planeCofficient)
                imageRepeatCount = 0
                for ilsdKey in imageLocationSorDisctionary.keys():
                    if image == imageLocationSorDisctionary[ilsdKey]:
                        imageRepeatCount+=1
                #assign all image to corresponding plane
                if imageRepeatCount == 0:
                    key = imageKey+planeKey
                    imageLocationSorDisctionary[key] = image
    return imageLocationSorDisctionary            
                
#distance between Rx and Tx-image(FOR) location is equal to path made by Rx and Tx(FOR)
def rxTxDistanceFor(receiverPath, imageLocationDictionary):
    rxTxDistanceForDictionary = {}
    for key in imageLocationDictionary.keys():
        val = imageLocationDictionary[key]
        rxTxImDistanceList = []
        for reLoc in receiverPath:
            rxTxImDistance  = distanceTo(val, reLoc)
            rxTxImDistanceList.append(rxTxImDistance)
        rxTxDistanceForDictionary[key] = rxTxImDistanceList
    return rxTxDistanceForDictionary       
 
