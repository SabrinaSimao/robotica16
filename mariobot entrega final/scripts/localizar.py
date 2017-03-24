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
fundo = None
cx = None
cy = None
radius = None
pos = [[0,0],[0,0]]
direction = 0
primeira = True
deslocamentos=[0,1000]
sumiu = True
size= 100;



def getOBJ(objeto,fundo,frame):
  global cx
  global cy
  global radius
  global pos
  global direction
  global deslocamentos
  global sumiu
  global primeira
  if objeto != None and fundo != None:
    #lower_yellow = np.array([150,0,50])
    #upper_yellow = np.array([169,255,255])
    #mask = cv2.inRange(hsv,lower_yellow,upper_yellow)
    objeto_gray = cv2.cvtColor(objeto,cv2.COLOR_BGR2GRAY)
    fundo_gray= cv2.cvtColor(fundo,cv2.COLOR_BGR2GRAY)
    w1 = cv2.subtract(objeto_gray,fundo_gray)
    w2 = cv2.subtract(fundo_gray,objeto_gray)
    mask = cv2.bitwise_or(w1, w2)
    ret ,mask = cv2.threshold(mask,np.percentile(mask, 95),255,cv2.THRESH_BINARY)
    kernel = np.ones((3,3),np.uint8)
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    close = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    cv2.imshow("mask",close)
    cv2.waitKey(1)
    res = cv2.bitwise_and(objeto,objeto,mask = close)
    cv2.imshow("res",res)
    cv2.waitKey(1)
    blur = cv2.GaussianBlur(res, (5,5),0)
    blur =  cv2.cvtColor(blur,cv2.COLOR_BGR2HSV)
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    hist = cv2.calcHist([blur],[0], close, [180], [1, 179] )
    cv2.normalize(hist,hist,0,255,cv2.NORM_MINMAX)
    dst = cv2.calcBackProject([frame],[0],hist,[0,180],1)
    kernel = np.ones((5,5),np.uint8)
    ret ,contornos = cv2.threshold(dst,np.percentile(dst, 95),255,cv2.THRESH_BINARY)
    opening = cv2.morphologyEx(contornos, cv2.MORPH_OPEN, kernel)
    close = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    mostrar= close
    contours, hierarchy = cv2.findContours(close,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    areas = sorted(contours, key=cv2.contourArea, reverse=True)
    print(len(areas) , " KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK")
    if len(areas) >=1:
      maior_area= cv2.contourArea(areas[0])
      indice = None
      for i in range(len(contours)):
        if cv2.contourArea(contours[i]) == maior_area:
          indice = i
          pass       
      cnt = contours[indice]
      (x,y),radius = cv2.minEnclosingCircle(cnt)
      center = (int(x),int(y))
      cx = center[0]
      cy = center[1]
      radius = int(radius)
      frame = cv2.cvtColor(frame,cv2.COLOR_HSV2RGB)
      cv2.circle(frame,center,radius,(255,255,255),2)  
      print("ELE ACHOU ALGUMA AREA") 
      cv2.imshow("back",frame)
      cv2.waitKey(1)
      if maior_area>300:
        if len(pos) <2:
          pos.append((cx,cy))
        else:
          pos[0] = pos[1]
          pos[1] = (cx,cy)

      deslocamento = ((pos[0][0]-pos[1][0])^2 + (pos[0][1]-pos[1][1])^2)^(1/2)
      print('DESLOCAMENTO: {0}'.format(deslocamento))
      if len(deslocamentos)<2:
        deslocamentos.append(deslocamento)
      else:
        deslocamentos[0] = deslocamentos[1]
        deslocamentos[1] = deslocamento

      if (len(pos)==2 and deslocamento > 50) or radius*2 < 100:
        cx = None
        cy = None
        radius = None
        sumiu = True
        print(".")
        if(sumiu):
            if pos[1][0]-pos[0][0] >  0:
              if primeira == 0:
                  direction= True
              print("robo sumiu para direita")
            else:
              if primeira == 0:
                 direction = False
              print("robo sumiu para esquerda")
            print("Procurando para {0}".format(direction)) 
            Follow.Search(direction)#nessa linha por Follow.Search(direction)
            primeira+=1
      else: 
        if abs(deslocamentos[1]-deslocamentos[0])<100:
          Follow.main(radius*2,(float(cx),float(cy)))
          print(cx,cy,radius*2)
          print("achei, estou seguindo!!")
          sumiu = False
          primeira = 0
      return cx,cy,radius
    else:
      direction = False
      print("procurando")
      Follow.Search(direction)
  else: 
    print("objeto e fundo ainda não aprendidos...")
  #cv2.imshow("back",frame)

def learn_background(frame):
	print("aprendeu fundooooooooooooooooo...............")
	global fundo
	fundo = frame
	return
def learn_obj(frame):
	print("aprendeu objetooooooooooooo....")
	global objeto
	objeto = frame
	return

def recebe(imagem):
	global cv_image
	global objeto
	global fundo
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
		#cv2.imshow("video", cv_image)		
		depois = time.clock()
		k = cv2.waitKey(1)
		if k==1048603:
			learn_background(cv_image)
		if k==1048691:
			learn_obj(cv_image)
		getOBJ(objeto,fundo,cv_image)
	except CvBridgeError as e:
		print(e)
def seguir_em_frente(s):
	global size;
	cx =320;
	cy = 240;
	k = cv2.waitKey(1)
	if k == ord('h'):
		size = 300
	if k == ord('p'):
		size = 100
	Follow.main(size,(cx,cy))

if __name__=="__main__":
	rospy.init_node("brain")
	recebedor = rospy.Subscriber("/camera/image_raw", Image, seguir_em_frente, queue_size=10, buff_size = 2**24)
	rospy.Subscriber("/scan", Follow.LaserScan, Follow.scaneou)
	rospy.Subscriber("/bump",Follow.Bump,Follow.bateu)

	#cv2.namedWindow("res")
	cv2.namedWindow("mask")
	#cv2.namedWindow("back")
	
	try:
		while not rospy.is_shutdown():
			Follow.Survival()
			rospy.sleep(0.1)
			#k = cv2.waitKey(1);
			k =cv2.waitKey(1)
			if k==1048486:
				Follow.toggleLaser()
	except rospy.ROSInterruptException:
		print("Ocorreu uma exceção com o rospy")

	
