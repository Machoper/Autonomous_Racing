#!/usr/bin/env python

import rospy
from race.msg import drive_param # import the custom message
import socket
import os
import subprocess

rospy.init_node('emergency', anonymous=True)
pub = rospy.Publisher('drive_parameters', drive_param, queue_size=10)

#the ip of the laptop
REMOTE_SERVER ='192.168.70.25'


def is_connected(hostname):
    # try:
    #     s = socket.create_connection((hostname, 1), 2) #hostname, x. x is the port number
    #     return True
    # except Exception as e:
    # 	print e
    #     pass
    # return False
    # res = os.system("ping -c 1 " + hostname)
    # if res == 0:
    # 	return True
    # else:
    # 	return False

    #since the package os is deprecated, use subprocess instead and mute the output to terminal
    p = subprocess.Popen(['ping', '-c', '1', hostname], stdout=subprocess.PIPE)
    p.wait()
    if p.poll() == 0:
    	return True
    else:
    	return False

while True:
    if (not is_connected(REMOTE_SERVER)):
    	print 'CONNECTION LOST'
        msg = drive_param()
        msg.velocity = 0
        msg.angle = 0
        pub.publish(msg)
    else:
    	pass
        # print('is connected')
