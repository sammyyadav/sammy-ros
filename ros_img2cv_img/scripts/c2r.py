#!/usr/bin/env python
from __future__ import print_function
 
import roslib

import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2

image_pub = rospy.Publisher("/usb_cam/image_raw",Image, queue_size=1)
rospy.init_node('image_feature', anonymous=True)
cap = cv2.VideoCapture(-1)
bridge = CvBridge()
while True:

	ret, frame = cap.read() 
	cv2.imshow("Image window", frame)
	image_pub.publish(bridge.cv2_to_imgmsg(frame, "bgr8"))
	if cv2.waitKey(1) & 0xFF == ord('q'): 
		break
cv2.destroyAllWindows()
