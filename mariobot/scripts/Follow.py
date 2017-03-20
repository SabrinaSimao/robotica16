#!/usr/bin/env python
# -*- coding:utf-8 -*- 
import roslib;
import rospy
import cv2

from geometry_msgs.msg import Twist, Vector3, Pose
from sensor_msgs.msg import LaserScan
from neato_node.msg import Bump

import sys, select, termios, tty

msg = """

"""
maxSize = 450
res = (640,480)
obj_global = None
middleZone = 20;
Ylimit = 50;
delta= None
speed = 1;
turnSpeed = 2.5;
useLaser = True;
escanned = False

#--
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
   
def applyLaser(wheel):

    global laserScan
    

    if(escanned):
    
        pathRecon = list(laserScan[315:]).extend(laserScan[:45])
        pathBack = laserScan[165:206]
        pathRight = laserScan[46:165]
        pathLeft = laserScan[206:315]

        lowerRecon = pathRecon
        lowerRecon.sort()
        lowerRecon = pathRecon.index(lowerRecon[0])
        lowerBack = pathBack
        lowerBack.sort()
        lowerBack = pathBack.index(lowerBack[0])
        lowerRight = pathRight
        lowerRight.sort()
        lowerRight = pathRight.index(lowerRight[0])
        lowerLeft = pathLeft
        lowerLeft.sort()
        lowerLeft = pathLeft.index(lowerLeft[0])

        if(pathRight[lowerRight] < 0.35 and pathRight[lowerRight] > 0.05):
            print("objeto a direita")
            wheel[1] -= 0.5
        if(pathLeft[lowerLeft] < 0.35 and pathLeft[lowerLeft] > 0.05):
            wheel[1] += 0.5
            
            print("objeto a esquerda")
        if(pathBack[lowerBack] < 0.3 and pathBack[lowerBack] > 0.05):
            print("correeee")
            wheel[0] += 0.5
            
        if(pathRecon[lowerRecon] < 1 and pathRecon[lowerRecon] > 0.1 and useLaser):
            lowerRecon /= 45
            lowerRecon -= 1
            
            speed = 1
            speed *= (1 - pathRecon[lowerRecon])
            speed += 0.5
            
            speed *= lowerRecon

            print(speed)
            wheel[1] -= speed  
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
