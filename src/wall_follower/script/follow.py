#!/usr/bin/python2
# -*- coding: utf-8 -*-

"""
authors: gokul, arpit, shreesh
"""

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

pub_ = None
regions_ = {
    'right': 0,
    'fright': 0,
    'front': 0,
    'fleft': 0,
    'left': 0,
}

state_ = 0

state_dict_ = {
    0: 'find the wall',
    1: 'turn left',
    2: 'follow the wall',
    3: 'turn right',
}

def clbk_laser(msg):
    global regions_
    regions_ = {
        'right':  min(min(msg.ranges[0:143]), 10),
        'fright': min(min(msg.ranges[144:287]), 10),
        'front':  min(min(msg.ranges[288:431]), 10),
        'fleft':  min(min(msg.ranges[432:575]), 10),
        'left':   min(min(msg.ranges[576:713]), 10),
    }

    take_action()

def change_state(state):
    global state_, state_dict_
    if state is not state_:
        state_ = state

def take_action():
    global regions_
    regions = regions_
    msg = Twist()
    linear_x = 0
    angular_z = 0
    
    state_description = ''
    
    d = 0.9

    # 0: 'find the wall',
    # 1: 'turn left',
    # 2: 'follow the wall',
    # 3: 'turn right'
    
    if regions['front'] > d and regions['fleft'] > d and regions['fright'] > d:
        s = 0 
    elif regions['front'] < d and regions['fleft'] > d and regions['fright'] > d:
        s = 1
    elif regions['front'] > d and regions['fleft'] > d and regions['fright'] < d:
        s = 1
    elif regions['front'] > d and regions['fleft'] < d and regions['fright'] > d:
        s = 2 
    elif regions['front'] < d and regions['fleft'] > d and regions['fright'] < d:
        s = 1
    elif regions['front'] < d and regions['fleft'] < d and regions['fright'] > d:
        s = 3
    elif regions['front'] < d and regions['fleft'] < d and regions['fright'] < d:
        s = 1
    elif regions['front'] > d and regions['fleft'] < d and regions['fright'] < d:
        s = 2
    else:
        state_description = 'unknown case'
        rospy.loginfo(regions)
    change_state(s)

def find_wall():
    msg = Twist()
    # msg.linear.x = 0.2
    msg.linear.x = 0.5
    # msg.angular.z = -0.3
    msg.angular.z = 0.6 #debug
    return msg

def turn_left():
    msg = Twist()
    msg.angular.z = 1.2
    return msg

def turn_right():
	msg = Twist()
	msg.angular.z = -0.3
	return msg

def follow_the_wall():
    global regions_
    
    msg = Twist()
    # msg.linear.x = 0.5
    msg.linear.x = 0.4
    return msg

def main():
    global pub_
    
    rospy.init_node('wall_follower')
    pub_ = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    sub = rospy.Subscriber('/baymax/laser/scan', LaserScan, clbk_laser)
    
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        msg = Twist()
        if state_ == 0:
            msg = find_wall()
        elif state_ == 1:
            msg = turn_left()
            rospy.Rate(1).sleep()
        elif state_ == 3:
        	msg = turn_right()
        elif state_ == 2:
            msg = follow_the_wall()
            pass
        else:
            rospy.logerr('Unknown state!')
        
        # debugging 
        global regions_
        regions = regions_
        print("left: {} | front: {} | right: {}".format(
        	round(regions['fleft'], 3),
        	round(regions['front'], 3),
        	round(regions['fright'], 3),
        	))
        print("============================================")

        pub_.publish(msg)
        
        rate.sleep()

if __name__ == '__main__':
    main()
