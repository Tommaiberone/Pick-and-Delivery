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
from Pick_and_Delivery.msg import NewGoal

DEBUG = True

class robot:

    Numero_comandi      = 0
    info_ricevute       = 0
    moving              = 0
    target_position     = numpy.empty(2,float)
    old_position        = numpy.empty(2,float)
    current_position    = numpy.empty(2,float)

def move_to_goal_callback(new_goal):

    if DEBUG: rospy.loginfo("Ho ricevuto una nuova destinazione\n")
    if DEBUG: rospy.loginfo("Mi dirigo alla posizione x:{}, y:{}".format(new_goal.x, new_goal.y))

    new_goal_msg.header.seq = robottino.Numero_comandi
    robottino.Numero_comandi+=1
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
    robottino.info_ricevute = 1

    robottino.target_position[0] = new_goal_msg.pose.position.x
    robottino.target_position[1] = new_goal_msg.pose.position.y


def position_callback(tf):

    transform_ok = transformCalculator.can_transform('map','base_link', rospy.Time(0))

    if transform_ok != 0:
        transformation = TransformStamped()
        transformation = transformCalculator.lookup_transform('map', 'base_link', rospy.Time(0))
        
        robottino.current_position[0] = transformation.transform.translation.x
        robottino.current_position[1] = transformation.transform.translation.y


def timer_check_status(event = None):

    if robottino.moving != 0:

        if math.sqrt(math.pow(robottino.current_position[0]-robottino.target_position[0], 2)+ 
                     math.pow(robottino.current_position[1]-robottino.target_position[1], 2)) < 1.5:

            rospy.loginfo("Sono arrivato a destinazione")

            publisher_check_status.publish("Arrived")
            robottino.moving = 0

def timer_incastrato_check(event = None):

    if robottino.moving != 0:

        position_x1 = robottino.current_position[0]
        position_y1 = robottino.current_position[1]
        if DEBUG: print("POSIZIONE CORRENTE: [{},{}]".format(position_x1, position_y1))

        sleep(5)

        position_x2 = robottino.current_position[0]
        position_y2 = robottino.current_position[1]
        if DEBUG: print("POSIZIONE CORRENTE: [{},{}]".format(position_x2, position_y2))

        if position_x1 == position_x2 and position_y1 == position_y2:

            rospy.loginfo("Sono bloccato!")
            publisher_check_status.publish('Stuck')
            robottino.moving = 0

#def distance_callback(pos):
 #   rospy.loginfo("Mi separa (distance dalla meta")
  #  dist = math.sqrt(math.pow(robottino.current_position[0]-pos.x, 2)+ math.pow(robottino.current_position[1]-pos.y, 2))
   # pubDist.publish(dist)
            

if __name__ == '__main__':
    
    try:
        rospy.init_node('set_goal', anonymous=True)

        new_goal_msg = PoseStamped()
        transformCalculator = tf2_ros.Buffer()
        liste = tf2_ros.TransformListener(transformCalculator)
        robottino = robot()

        rate = rospy.Rate(10)

        publisher_posizione         = rospy.Publisher(  "/move_base_simple/goal",    PoseStamped,    queue_size=10)
        publisher_check_status      = rospy.Publisher(  "/Arrived",                  String,         queue_size=10)

        subscriber_new_goal         = rospy.Subscriber( 'New_Goal',                  NewGoal,        move_to_goal_callback)
        subscriber_tf               = rospy.Subscriber( 'tf',                        TFMessage,      position_callback)

        timer_arrivato              = rospy.Timer(      rospy.Duration(0.5),                         timer_check_status)
        timer_incastrato            = rospy.Timer(      rospy.Duration(6),                           timer_incastrato_check)

        while not rospy.is_shutdown():
            if robottino.info_ricevute != 0:
                publisher_posizione.publish(new_goal_msg)
            rate.sleep()

    except rospy.ROSInterruptException:
        pass











































