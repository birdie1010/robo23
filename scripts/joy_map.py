#!/usr/bin/env python
# license removed for brevity


#keep analog mode on in controller



import rospy
from std_msgs.msg import String
from std_msgs.msg import Int32

from sensor_msgs.msg import Joy

from geometry_msgs.msg import Quaternion

loco = Quaternion()
yaw= Int32()
pitch= Int32()
yaw_lock=0  #0 locked 1 unlocked
pitch_lock=0

def map_range(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def changer(value): 
    if(value==0):
        value=1
        print('unlocked')
    elif(value==1):
        value=0
        print('locked')
    else:
        rospy.loginfo("error in changer")
        rospy.signal_shutdown
    return value



def loco_finder(data):
    global loco
    loco.z=0
    loco.x=-data.axes[0]
    loco.y=data.axes[1]
    if(data.buttons[0]==1):
        loco.w=1
    elif(data.buttons[1]==1):
        loco.w=-1
    else:
        loco.w=0
    

def yp_finder(data):
    global yaw,pitch,lock,yaw_lock,pitch_lock
    yaw_decimal=-data.axes[3]
    pitch_decimal=data.axes[4]
    if(yaw_lock==1):
        yaw.data=int(map_range(yaw_decimal,-1,1,-30,30))
    if(pitch_lock==1):
        pitch.data=int(map_range(pitch_decimal,-1,1,30,60))

def 

    
    
    



def joy_callback(data):
    global yaw_lock,pitch_lock
    loco_finder(data)
    # rospy.loginfo(data.axes)
    if(data.buttons[5]==1):
        yaw_lock=changer(yaw_lock)
    if(data.buttons[7]==1):
        pitch_lock=changer(pitch_lock)
    yp_finder(data)


def talker():
    rospy.Subscriber('joy', Joy, joy_callback)
    pub_loco = rospy.Publisher('locomotion', Quaternion, queue_size=10)
    pub_yaw = rospy.Publisher('target_yaw', Int32, queue_size=10)
    pub_pitch = rospy.Publisher('target_pitch', Int32, queue_size=10)

    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        # hello_str = "hello world %s" % rospy.get_time()
        # rospy.loginfo(hello_str)
        pub_loco.publish(loco)
        pub_yaw.publish(yaw)
        pub_pitch.publish(pitch)    
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass