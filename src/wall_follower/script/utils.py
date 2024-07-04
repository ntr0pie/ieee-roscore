import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry


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
        print('Wall follower - [%s] - %s' % (state, state_dict_[state]))
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
        rospy.loginfo(regions)
    change_state(s)
    print("STATE: {}".format(state_description))


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
