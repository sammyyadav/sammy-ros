import sys
import cv2 
import matplotlib.pyplot as plt
import numpy as np
import time
import os
import math
import random
import rospy

from std_msgs.msg import UInt16

rospy.init_node('GAME', anonymous=True)

img = cv2.imread("/home/sammy-ros/catkin_ws/src/ros_game/src/a.jpeg")
img = img[100:200,100:200]
img = cv2.resize(img,(640,480))
cv2.rectangle(img,(0,0),(640,450),(0,0,0),-1) 
img = cv2.line(img, (0,450), (640,450), (0,0,255), 5)
cv2.putText(img, "Score :" , (10 , 475) , cv2.FONT_HERSHEY_SIMPLEX,0.7,(0, 0 , 0),2) #font stroke


def start(img):
    img2 = img.copy()


    cv2.rectangle(img2,(288,445),(352,450),(0,255,255),-1)    
    img2 = cv2.circle(img2, (320,435),10 , (255,0,0), -1)
    prev = time.time()
    i = 3
    position = (310,230)
    while i != -1 :
        img1 = img2.copy() 
        if  i == 0: 
            i = "Start"
            position = (280 ,230)
        cv2.putText(img1, str(i) , position , cv2.FONT_HERSHEY_SIMPLEX,1,(0, 255 , 0),3) #font stroke
        cv2.imshow("Game",img1)
        cv2.waitKey(125)
        cur = time.time()

        if cur- prev >= 1 and i != "Start":
            prev = cur
            i-=1
        elif i == "Start" : 
            if cur- prev >= 1 :
                prev = cur
                break

    cv2.putText(img2, "" , position , cv2.FONT_HERSHEY_SIMPLEX,1,(209, 80, 0, 255),3) #font stroke       
    #return img
    
start(img)
theta = random.randint(30,60)

def new_position(theta):
    #print theta
    if theta < 90:
        if theta < 45:
            dx = 5
            dy = round(dx * math.tan(math.radians(theta)),0)
        elif theta > 45:
            dy = 5
            dx = round(dy * math.tan(math.radians(theta)),0)
        elif theta == 45:
         return (5,5)

    else:

        if theta < 225:
            dx = -5
            dy =round( dx * math.tan(math.radians(theta)),0)
        elif theta > 225:
            dy = -5
            dx = round( dy * math.tan(math.radians(theta)),0)
        elif theta == 225: return (-5,-5)
    return (int(dx),int(dy)) 

(dx,dy) = new_position(theta)   
#print (dx,dy)
def moveball(img, points, (x,y),pl,dx,dy):
    h , w = 6 , 64
        
    while  True:
        img2 = img.copy()
        nx = x+dx
        if nx < 0: nx = 1
        ny = y-dy
        if ny < 0: ny = 1
        if ny > 437: ny = 435
        position = (nx,ny)
        img2 = cv2.circle(img2, position ,10 , (255,0,0), -1)
        cv2.rectangle(img2,pl,(pl[0]+w,pl[1]+h),(255,255,0),-1)
        cv2.putText(img2, str(points) , (100,475) , cv2.FONT_HERSHEY_SIMPLEX,0.7,( 0, 0, 0), 2) #font stroke       


        cv2.imshow("Game",img2)
        cv2.waitKey(125)
        return position

position = (320,435)


pl = (288,445)


def callback(msg):
    
    global pl
    pl = (msg.data,445)
    

points = 0

while True:
    imgc = img.copy()
    rospy.Subscriber("/chatter",UInt16,callback)
    position = moveball(imgc, points ,position,pl,dx,dy)
    

    
    if position[0] >= 635 and dy > 0 :
        theta = 90 + theta
        (dx,dy) = new_position(theta)
    elif position[0] >= 635 and dy < 0 :
            theta = 540 - theta
            (dx,dy) = new_position(theta)


    elif position[1]<= 2  and dx < 0:
        theta = 90 + theta
        (dx,dy) = new_position(theta)
    elif position[1] <= 2  and dx > 0:
        theta = 360 - theta
        (dx,dy) = new_position(theta)


    elif position[0] <= 2  and dy < 0 :
        theta = 540 - theta 
        (dx,dy) = new_position( theta)

    elif position[0] <= 2  and dy > 0 :
        theta = 180 - theta
        (dx,dy) = new_position(theta)


    elif position[1]>= 435 and position[0] >= pl[0] and position[0]<=pl[0]+64  and dx < 0:
        theta =  theta - 90
        (dx,dy) = new_position(theta)
        points += 5
    elif position[1]>= 435 and position[0] >= pl[0] and position[0]<=pl[0]+64 and dx > 0:
            theta = 360 - theta
            (dx,dy) = new_position(theta)
            points+=5

    elif  position[1]>= 435: break


    
    if cv2.waitKey(5) and 0xFF == 27:
        break

def end(img):
    img2 = img.copy()
    prev = time.time()
    i = 3
    position = (250 ,230)
    while i != -1 :
        img1 = img2.copy() 
        if  i == 0: 
            i = "Start"
            position = (250 ,230)
        cv2.putText(img1, "Game Over" , position , cv2.FONT_HERSHEY_SIMPLEX,1,(0, 0, 255),2) #font stroke
        cv2.putText(img1, "Your Score = "+ str(points) , (200,275) , cv2.FONT_HERSHEY_SIMPLEX,1,(255, 0, 0),2) #font stroke
        cv2.imshow("Game",img1)
        cv2.waitKey(125)
        cur = time.time()

        if cur- prev >= 1 and i != "Start":
            prev = cur
            i-=1
        elif i == "Start" : 
            if cur- prev >= 1 :
                prev = cur
                break

    cv2.putText(img2, "" , position , cv2.FONT_HERSHEY_SIMPLEX,1,(209, 80, 0, 255),) #font stroke       
    #return img
    
end(img)


    
cv2.destroyAllWindows()
