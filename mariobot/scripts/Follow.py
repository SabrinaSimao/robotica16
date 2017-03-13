
import roslib; roslib.load_manifest('teleop_twist_keyboard')
import rospy

from geometry_msgs.msg import Twist, Vector3, Pose

import sys, select, termios, tty

msg = """

"""
maxSize = 450
res = (640,480)

middleZone = 20;
Ylimit = 50;

speed = 1;
turnSpeed = 0.5;

#--
aborted = False
laserScan = [];

def main(size, pos):
    wheel = (0,0)
    if(aborted):
        return;
        
    Survival()
    
    if(size > maxSize or pos[1] <= Ylimit):
        SendSpeed(wheel)
        return
    
    wheel += (speed,0)
    obgDist = pos[0] - (res[0] / 2)
    right = obgDist >= 0
    
    if(right):
        if(obgDist >= middleZone):
            delta = turnSpeed * (obgDist / (res[0] / 2))
            wheel += (0,-delta)
    else:
        if(abs(obgDist) >= middleZone):
            delta = turnSpeed * (abs(obgDist) / (res[0] / 2))
            wheel += (0,delta)
    
    
def SendSpeed(wheel):
    
    vel = Twist(Vector3(wheel[0],0,0),Vector3(0,0,wheel[1]))    
    velocidadeFinal = rospy.Publisher("/cmd_vel", Twist, queue_size = 1)
    
    velocidadeFinal.publish(vel)
    
    return
    #função que manda pro robo as velocidades de cada roda
    
def scaneou(laser):
    global laserScan
    laserScan = laser.rangers
    
    
def Survival():
    global laserScan
    rospy.Subscriber("/scan", LaserScan, scaneou)
    print(laserScan)
    bumper = [0,0] #pegar bumper dps !!!!!!!!
    
    if(bumper[0] == 1 or bumber[1] == 1):
        Abort();

def Abort():
    global aborted
    aborted = True
    #dar ré por um tempo e virar um pouco
    #aborted = False

def Search(right):
    if(right):
        SendSpeed([0,-0.1])
    else:
        SendSpeed([0,0.1])
