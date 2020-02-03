#!/usr/bin/env python

import rospy
from race.msg import drive_values
from race.msg import drive_param
from std_msgs.msg import Bool


"""
What you should do:
 1. Subscribe to the keyboard messages (If you use the default keyboard.py, you must subcribe to "drive_paramters" which is publishing messages of "drive_param")
 2. Map the incoming values to the needed PWM values
 3. Publish the calculated PWM values on topic "drive_pwm" using custom message drive_values
"""
class Talker():
    def __init__(self):
        rospy.init_node('talker')
        self.pub = rospy.Publisher('drive_pwm', drive_values, queue_size=10)
        rospy.Subscriber('drive_parameters', drive_param, self.cb)
        rospy.spin()

    def paramToPwm(self, val):
        return int(6554 + (val+100)/200*(13108-6554))

    def cb(self, data):
        pwm_vel = self.paramToPwm(data.velocity)
        pwm_angle = self.paramToPwm(data.angle)
        msg = drive_values(pwm_angle, pwm_vel)
        self.pub.publish(msg)


t = Talker()

