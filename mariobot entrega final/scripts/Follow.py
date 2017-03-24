#!/usr/bin/env python
# -*- coding:utf-8 -*- 
import roslib;
import rospy
import cv2

from geometry_msgs.msg import Twist, Vector3, Pose
from sensor_msgs.msg import LaserScan
from neato_node.msg import Bump
import numpy as np
import sys, select, termios, tty

msg = """

"""
maxSize = 250
res = (640,480)
obj_global = None
middleZone = 20;
Ylimit = 50;
delta= None
speed = 0.3;
turnSpeed = 2.5;
useLaser = True;
escanned = False
aborted = False
laserScan = [];
batidas = [];

def main(size, pos):
    print("main")
    wheel = [0,0]
    global delta
    if(aborted):
        print("bebe chutado")
        return;
        
       
    if(size > maxSize or pos[1] <= Ylimit):
        SendSpeed(wheel)
        return
    
    wheel = [speed,0]
    obgDist = pos[0] - (res[0] / 2)
    

    
    delta = -turnSpeed * (float(obgDist / (res[0] / 2)))

    wheel = [speed, delta]

    wheel = applyLaser(wheel)

    


    print(wheel)
    SendSpeed(wheel);
    print(delta)

def toggleLaser():
    global useLaser
    useLaser = not useLaser

def getMin(lista):
	minV = 10
	index = 0
	count = 0
	for i in lista:
		if (i < minV) and (i > 0.2):
			minV = i
			index = count
		count += 1
	return(minV,index)
   
def applyLaser(wheel):

    global laserScan

    if (escanned):
        laserScanlist = list(laserScan)
        temp = list(laserScan[330:])
        temp.extend(laserScan[:30])
        indexlist = []
        for i in range(len(temp)):
            if temp[i] < 0.25:
            	indexlist.append(i)

        for j in range(len(indexlist)):
            temp.pop(indexlist[-j -1])
                
        print(temp)

        print(indexlist, " IDEX LIST")
        meanRecon = np.mean(temp)
	
        pathRecon = list(laserScanlist[315:])
        pathRecon.extend(laserScanlist[:45])
        pathBack = list(laserScanlist[165:206])
        pathRight = list(laserScanlist[46:165])
        pathLeft = list(laserScanlist[206:315])
        
	
        lowerRecon = getMin(pathRecon)
        print(lowerRecon , " 00000000000000000000")
        lowerBack = getMin(pathBack)
        lowerRight = getMin(pathRight)
        lowerLeft = getMin(pathLeft)

        if(lowerRight[0] < 0.75 ):
            print("objeto a direita XXXXXXXXXXXXXXXX")
            print(lowerRight, " direita ");
            wheel[1] -= 1.5 * (0.75 - lowerRight[0])

        if(lowerLeft[0] < 0.75 ):
            wheel[1] += 1.5 * (0.75 - pathLeft[lowerLeft])
            print("objeto a esquerda XXXXXXXXXXXXXX")
            print(lowerLeft, " Left");

        if(lowerBack[0] < 0.5 ):
            print("correeee XXXXXXXXXXXXXXX")
            print(lowerBack, " Back ");
            wheel[0] += 1
            
        if(lowerRecon[0] < 1.5 and useLaser):
            print("EVADE PORRA")

            lower = lowerRecon[1]
            lower /= 45
            lower -= 1
            
            
            
            speed = 1
            speed *= (1.5 - lowerRecon[0])
            
            print(lowerRecon, " Recon")
            print(speed)
            wheel[1] -= speed  
        print(meanRecon, 'media frontal')
        if(meanRecon < 0.6):
        	wheel = [0,0]
    return wheel
        
        
        
    
def SendSpeed(wheel):
    
    vel = Twist(Vector3(wheel[0],0,0),Vector3(0,0,wheel[1]))    
    velocidadeFinal = rospy.Publisher("/cmd_vel", Twist, queue_size = 1)
    
    velocidadeFinal.publish(vel)
    
    #função que manda pro robo as velocidades de cada roda
    
def scaneou(laser):
    global laserScan
    global escanned
    laserScan = laser.ranges
    escanned = True

def bateu(bump_obj):
    global obj_global
    obj_global = bump_obj
    
def Survival():
    if(not aborted):
        #print(laserScan)
        
        if obj_global != None:
            if  obj_global.rightFront==1:
                print("Bateu frente direita")
                SendSpeed([-1,-3])
                Abort(1.5)
            elif  obj_global.leftFront==1 :
                print("Bateu frente esquerda")
                SendSpeed([-1,3])    
                Abort(1.5)  

    

def Abort(time):
    global aborted
    global obj_global
    aborted = True
    print("estou abortando")
    cv2.waitKey(1000)
    aborted = False
    print("Desabortei")
    #dar ré por um tempo e virar um pouco
    #aborted = False

def Search(right):
    if(aborted):
        print("bebe chutado")
        return;
        
    if(right):
        SendSpeed([0,-0.3])
    else:
        SendSpeed([0,0.3])
