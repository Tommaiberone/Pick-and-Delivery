#!/usr/bin/env python2

import numpy
import math 
from time import sleep
from std_msgs.msg import String, Float32
import rospy
from geometry_msgs.msg import TransformStamped
from geometry_msgs.msg import PoseStamped
from tf2_msgs.msg import TFMessage
import tf2_ros
from set_goal.msg import NewGoal

class elem:
    published = 0
    moving = 0
    tar_position= numpy.empty(2,float)
    old_position= numpy.empty(2,float)
    cur_position= numpy.empty(2,float)

n=0

def move_to_goal_callback(new_goal):

    rospy.loginfo("sono qui")

    new_goal_msg.header.seq = n
    n+=1
    new_goal_msg.header.stamp = rospy.Time.now()
    new_goal_msg.header.frame_id = "/map"
    
    new_goal_msg.pose.position.x = new_goal.x
    new_goal_msg.pose.position.y = new_goal.y
    new_goal_msg.pose.position.z = 0
    
    new_goal_msg.pose.orientation.x = 0
    new_goal_msg.pose.orientation.y = 0
    new_goal_msg.pose.orientation.z = 0
    new_goal_msg.pose.orientation.w = new_goal.theta

    e.moving = 1
    e.published = 1

    e.tar_position[0] = new_goal_msg.pose.position.x
    e.tar_position[1] = new_goal_msg.pose.position.y


def position_callback(tf):
    transform_ok = tfBuffer.can_transform('map','base_link', rospy.Time(0))
    if transform_ok != 0:
        trasStamp = TransformStamped()
        trasStamp =tfBuffer.lookup_transform('map', 'base_link', rospy.Time(0))
        
        e.cur_position[0] = trasStamp.transform.translation.x
        e.cur_position[1] = trasStamp.transform.translation.y


def timer_callback(event = None):
    if e.moving != 0:
        if math.sqrt(math.pow(e.cur_position[0]-e.tar_position[0], 2)+ math.pow(e.cur_position[1]-e.tar_position[1], 2)) < 1.5:
            rospy.loginfo("Sono arrivato a destinazione")
            pubArr.publish("Arrived")
            e.moving = 0

def timer2_callback(event = None):
    if e.moving != 0:
        pos1 = e.cur_position [0]
        print(pos1)
        sleep(5)
        pos2 = e.cur_position [1]
        print(pos2)
        if pos1 == pos2:
            rospy.loginfo("Sono bloccato!")
            pubArr.publish('Stuck')
            e.moving = 0

def distance_callback(pos):
    rospy.loginfo("sono qui (distance")
    dist = math.sqrt(math.pow(e.cur_position[0]-pos.x, 2)+ math.pow(e.cur_position[1]-pos.y, 2))
    pubDist.publish(dist)
            

if __name__ == '__main__':
    try:

        rospy.init_node('set_goal', anonymous=True)

        new_goal_msg = PoseStamped()
        tfBuffer = tf2_ros.Buffer()
        liste = tf2_ros.TransformListener(tfBuffer)
        e = elem()

        rate = rospy.Rate(10)

        pub = rospy.Publisher("/move_base_simple/goal", PoseStamped, queue_size=10)
        pubGoal = rospy.Publisher("/Listener", String, queue_size=10)
        pubArr = rospy.Publisher("/Arrived", String, queue_size=10)
        pubDist = rospy.Publisher("DistancePub", Float32, queue_size=10)

        sub = rospy.Subscriber('New_Goal', NewGoal, move_to_goal_callback)
        sub_dist = rospy.Subscriber('DistanceSub', NewGoal, distance_callback)
        sub_tf = rospy.Subscriber('tf', TFMessage, position_callback)

        timer = rospy.Timer(rospy.Duration(0.5), timer_callback)
        timer2 = rospy.Timer(rospy.Duration(6), timer2_callback)

        while not rospy.is_shutdown():
            if e.published != 0:
                pub.publish(new_goal_msg)
            rate.sleep()

    except rospy.ROSInterruptException:
        pass











































