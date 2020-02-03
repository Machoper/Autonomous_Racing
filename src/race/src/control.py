#!/usr/bin/env python

import rospy
from race.msg import drive_param
from race.msg import pid_input

kp = 14.0 # 20
kd = 0.09 # 0.9
servo_offset = 18.5	# zero correction offset in case servo is misaligned. 
prev_error = 0.0 
vel_input = 8.0 # 8

pub = rospy.Publisher('drive_parameters', drive_param, queue_size=1)

def vel(angle):
	if abs(angle) < 15:
		return 15
	else:
		return 8

def control(data):
	# global prev_error
	# global vel_input
	# global kp
	# global kd

	kp = 14.0 # 20
	kd = 0.09 # 0.9
	servo_offset = 18.5	# zero correction offset in case servo is misaligned. 
	prev_error = 0.0 
	vel_input = 8.0 # 8

	## Your code goes here
	# 1. Scale the error
	# 2. Apply the PID equation on error
	# 3. Make sure the error is within bounds

	# error = data.pid_error * 10
	error = data.pid_error * 5
	control_error = kp * error + kd * (prev_error - error)
	# angle = kp*error + kd*(error-prev_error)
	angle = 0 - (control_error - servo_offset)
	# angle = control_error
	#angle = control_error - servo_offset
	# angle = servo_offset - control_error
	prev_error = error

	# angle *= 1.5

	if angle > 100:
		angle = 100
	elif angle < -100:
		angle = -100
	
	print "error: ", data.pid_error
	print "ce: ", control_error
	print "angle: ", angle
	# variable velocity handled in dist_finder.py
	print "velocity: ", data.pid_vel
	## END

	msg = drive_param();
	msg.velocity = data.pid_vel
	msg.angle = angle
	pub.publish(msg)

if __name__ == '__main__':
	print("Listening to error for PID")
	rospy.init_node('pid_controller', anonymous=True)
	rospy.Subscriber("error", pid_input, control)
	rospy.spin()
