#!/usr/bin/env python

import rospy
import math
from sensor_msgs.msg import LaserScan
from race.msg import pid_input

# Some useful variable declarations.
angle_range = 240	# sensor angle range of the lidar
car_length = 1.5	# distance (in m) that we project the car forward for correcting the error. You may want to play with this. 
desired_trajectory = 1.25	# distance from the wall (left or right - we cad define..but this is defined for right)
vel = 15 
error = 0.0
delay = .01

pub = rospy.Publisher('error', pid_input, queue_size=10)

##	Input: 	data: Lidar scan data
##			theta: The angle at which the distance is requried
##	OUTPUT: distance of scan at angle theta
def getRange(data,theta):
# Find the index of the arary that corresponds to angle theta.
# Return the lidar scan value at that index
# Do some error checking for NaN and ubsurd values
## Your code goes here
		index = (theta + 30) * (len(data.ranges)/240) 
		# print theta, " - ", data.ranges[index]
		dist = data.ranges[index]
		if math.isnan(dist):
			return 4
		else:
			return dist

def calc_error(theta, a, b):
	swing = math.radians(theta)
	
	## Your code goes here
	alpha = math.atan2(a*math.cos(swing) - b, a*math.sin(swing)) +.2
	#print a*math.cos(swing) - b
	#print a*math.sin(swing)
	print "alpha: ", alpha
	AB = b*math.cos(alpha) #original distance from wall
	AC =  car_length #distance offset...this is arbitrary, may have to play with this!
	CD = AB + AC * math.sin(alpha) #updated distance from wall

	error = desired_trajectory - CD

	return error

def callback(data):
	theta = 45
	a = getRange(data, theta)		# distance at angle
	b = getRange(data, 0)			# distance to wall
	c = getRange(data, 90)			# distance straight ahead
	# print "a: ", a, "b: ", b
	
	# ## Your code goes here

	error = calc_error(theta, a, b)

	vel = 20 - 1.6*abs(error)

	# if c < 1.7 or a < .5:
	if c < 1.7 or a < .7: 	# if wall within 1.7 units or wall at angle within .7
		error *= 4		  	# multiply error
		vel = 8				# set velocity to min
	

	# 8 = lowest forwards
	# -10 = lowest backwards


	msg = pid_input()
	msg.pid_error = error
	msg.pid_vel = vel
	pub.publish(msg)
	

if __name__ == '__main__':
	print("Laser node started")
	rospy.init_node('dist_finder',anonymous = True)
	rospy.Subscriber("scan",LaserScan,callback)
	rospy.spin()
