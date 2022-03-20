#!/usr/bin/env python

import numpy
import math 
from time import sleep
from std_msgs.msg import String, Float32
import rospy
from geometry_msgs.msg import TransformStamped
from geometry_msgs.msg import PoseStamped
from tf2_msgs.msg import TFMessage
import tf2_ros
from Pick_and_Delivery.msg import NewGoal

class robot:

    published           = 0
    moving              = 0
    target_position     = numpy.empty(2,float)
    old_position        = numpy.empty(2,float)
    current_position    = numpy.empty(2,float)

def move_to_goal_callback(new_goal, Numero_comandi):

    rospy.loginfo("sono qui")

    new_goal_msg.header.seq = Numero_comandi
    Numero_comandi+=1
    new_goal_msg.header.stamp = rospy.Time.now()
    new_goal_msg.header.frame_id = "/map"
    
    new_goal_msg.pose.position.x = new_goal.x
    new_goal_msg.pose.position.y = new_goal.y
    new_goal_msg.pose.position.z = 0
    
    new_goal_msg.pose.orientation.x = 0
    new_goal_msg.pose.orientation.y = 0
    new_goal_msg.pose.orientation.z = 0
    new_goal_msg.pose.orientation.w = new_goal.theta

    robottino.moving = 1
    robottino.published = 1

    robottino.target_position[0] = new_goal_msg.pose.position.x
    robottino.target_position[1] = new_goal_msg.pose.position.y


def position_callback(tf):
    transform_ok = tfBuffer.can_transform('map','base_link', rospy.Time(0))
    if transform_ok != 0:
        trasStamp = TransformStamped()
        trasStamp =tfBuffer.lookup_transform('map', 'base_link', rospy.Time(0))
        
        robottino.current_position[0] = trasStamp.transform.translation.x
        robottino.current_position[1] = trasStamp.transform.translation.y


def timer_arrivato_check(event = None):
    if robottino.moving != 0:
        if math.sqrt(math.pow(robottino.current_position[0]-robottino.target_position[0], 2)+ 
                     math.pow(robottino.current_position[1]-robottino.target_position[1], 2)) < 1.5:
            rospy.loginfo("Sono arrivato a destinazione")
            publisher_arrivato_check.publish("Arrived")
            robottino.moving = 0

def timer_incastrato_check(event = None):
    if robottino.moving != 0:
        pos1 = robottino.current_position [0]
        print(pos1)
        sleep(5)
        pos2 = robottino.current_position [1]
        print(pos2)
        if pos1 == pos2:
            rospy.loginfo("Sono bloccato!")
            publisher_arrivato_check.publish('Stuck')
            robottino.moving = 0

def distance_callback(pos):
    rospy.loginfo("sono qui (distance")
    dist = math.sqrt(math.pow(robottino.current_position[0]-pos.x, 2)+ math.pow(robottino.current_position[1]-pos.y, 2))
    pubDist.publish(dist)
            

if __name__ == '__main__':

    Numero_comandi=0
    
    try:
        rospy.init_node('set_goal', anonymous=True)

        new_goal_msg = PoseStamped()
        tfBuffer = tf2_ros.Buffer()
        liste = tf2_ros.TransformListener(tfBuffer)
        robottino = robot()

        rate = rospy.Rate(10)

        publisher_posizione         = rospy.Publisher("/move_base_simple/goal", PoseStamped, queue_size=10)
        pubGoal                     = rospy.Publisher("/Listener", String, queue_size=10)
        publisher_arrivato_check    = rospy.Publisher("/Arrived", String, queue_size=10)
        pubDist                     = rospy.Publisher("DistancePub", Float32, queue_size=10)

        sub                         = rospy.Subscriber('New_Goal', NewGoal, move_to_goal_callback, callback_args=Numero_comandi)
        sub_dist                    = rospy.Subscriber('DistanceSub', NewGoal, distance_callback)
        sub_tf                      = rospy.Subscriber('tf', TFMessage, position_callback)

        timer_arrivato              = rospy.Timer(rospy.Duration(0.5), timer_arrivato_check)
        timer_incastrato            = rospy.Timer(rospy.Duration(6), timer_incastrato_check)

        while not rospy.is_shutdown():
            if robottino.published != 0:
                publisher_posizione.publish(new_goal_msg)
            rate.sleep()

    except rospy.ROSInterruptException:
        pass











































