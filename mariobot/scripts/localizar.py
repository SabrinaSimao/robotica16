#!/usr/bin/env python
# -*- coding:utf-8 -*- 
import rospy
import cv2
import numpy as np
import time
from sensor_msgs.msg import Image
from cv_bridge import CvBridge,CvBridgeError
import Follow

bridge = CvBridge()
atraso = 1.5
objeto = None
cx = None
cy = None
radius = None
pos = [[0,0],[0,0]]
direction = 0
primeira = True

def getOBJ(foto,foto1):
	global cx
	global cy
	global radius
	global pos
	if foto != None:
		foto = cv2.cvtColor(foto, cv2.COLOR_RGB2HSV)
		hist = cv2.calcHist([foto],[0], None, [180], [1, 170] )
		cv2.normalize(hist,hist,0,255,cv2.NORM_MINMAX)
		foto1 = cv2.cvtColor(foto1, cv2.COLOR_RGB2HSV)
		dst = cv2.calcBackProject([foto1],[0],hist,[0,180],1)
		kernel = np.ones((5,5),np.uint8)
		opening = cv2.morphologyEx(dst, cv2.MORPH_OPEN, kernel)
		lower = cv2.cv.Scalar(100)
		higher = cv2.cv.Scalar(255)
		mask = cv2.inRange(opening, lower, higher)

		mask_video = bridge.imgmsg_to_cv2(mask, "bgr8")
        cv2.imshow("mask", mask_video)
		
		contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		areas = sorted(contours, key=cv2.contourArea, reverse=True)
		maior_area= cv2.contourArea(areas[0])
		maior_area
		indice = None
		for i in range(len(contours)):
			if cv2.contourArea(contours[i]) == maior_area:
				indice = i
				pass       
		cnt = contours[indice]
		M = cv2.moments(cnt)  
		cx = int(M['m10']/M['m00'])
		cy = int(M['m01']/M['m00']) 
		(x,y), radius = cv2.minEnclosingCircle(cnt)
		#center = (int(x),int(y))
		radius = int(radius)
		if len(pos) <2:
			pos.append((cx,cy))
		else:
			pos[0] = pos[1]
			pos[1] = (cx,cy)

		deslocamento = ((pos[0][0]-pos[1][0])^2 + (pos[0][1]-pos[1][1])^2)^(1/2)

		if len(pos)==2 and deslocamento > 500:
			cx = None
			cy = None
			radius = None
			print(".")
			if pos[1][0]-pos[0][0] >  0:
				direction= 1
				Follow.Search(direction)
			else:
				direction = 0
				Follow.Search(direction)
			print("sumiu, vou procurar")
		else:
			print("achei!!")

		return cx,cy,radius
	else:
		print("A imagem ainda não foi aprendida")
		return 0

def learnOBJ(imagem_capturada):
    global objeto
    objeto = imagem_capturada
	print("capturou a imagem")
    return 

def recebe(imagem):
    global cv_image
    global objeto
    global primeira
    now = rospy.get_rostime()
    imgtime = imagem.header.stamp
    lag = now-imgtime
    delay = (lag.secs+lag.nsecs/1000000000.0)
    if delay > atraso:
        return 
    print("DELAY", delay)
    try:
        antes = time.clock()
        cv_image = bridge.imgmsg_to_cv2(imagem, "bgr8")
        cv2.imshow("video", cv_image)
		if primeira == True:
				k = cv2.waitKey(1)
				if (k == 27):         # wait for ESC key to exit
					learnOBJ(cv_image)
					primeira = False	
		
		depois = time.clock()
		getOBJ(objeto,cv_image)
		#("TEMPO", depois-antes)
    except CvBridgeError as e:
        print(e)
	    
if __name__=="__main__":
	rospy.init_node("brain")
	recebedor = rospy.Subscriber("/camera/image_raw", Image, recebe, queue_size=10, buff_size = 2**24)
	cv2.namedWindow("video")
	cv2.namedWindow("mask")
	try:
		while not rospy.is_shutdown():
			if cx!=None and cy != None:
				Follow.main(radius*2,(cx,cy))		
			rospy.sleep(0.1)

	except rospy.ROSInterruptException:
	    print("Ocorreu uma exceção com o rospy")

	
