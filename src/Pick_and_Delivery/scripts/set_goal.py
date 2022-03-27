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

DEBUG = True

#Crea la classe robot, che immagazzina dei parametri di controllo e
#i parametri necessari alla navigazione
class robot:

    Numero_comandi_ricevuti = 0
    info_ricevute           = False
    moving                  = False
    target_position         = numpy.empty(2,float)
    old_position            = numpy.empty(2,float)
    current_position        = numpy.empty(2,float)


#Funzione di callback per il listener del topic \NewGoal
#Se arriva un nuovo messaggio su tale topic vengono impostati,
#sulla base del contenuto del messaggio stesso:
#   -   i campi del messaggio new_goal_msg
#   -   i parametri di controllo del robottino
def move_to_goal_callback(new_goal):

    if DEBUG: print("Ho ricevuto una nuova destinazione\n")
    if DEBUG: print("Mi dirigo alla posizione x:{}, y:{}".format(new_goal.x, new_goal.y))

    #Imposta i parametri del messaggio new_goal_msg come quelli ricevuti
    new_goal_msg.header.seq = robottino.Numero_comandi_ricevuti
    new_goal_msg.header.stamp = rospy.Time.now()
    new_goal_msg.header.frame_id = "/map"
    
    new_goal_msg.pose.position.x = new_goal.x
    new_goal_msg.pose.position.y = new_goal.y
    new_goal_msg.pose.position.z = 0
    
    new_goal_msg.pose.orientation.x = 0
    new_goal_msg.pose.orientation.y = 0
    new_goal_msg.pose.orientation.z = 0
    new_goal_msg.pose.orientation.w = new_goal.theta

    #Imposta i parametri di controllo del robottino
    robottino.Numero_comandi_ricevuti+=1
    robottino.moving = True
    robottino.info_ricevute = True

    #Imposta i parametri di navigazione del robottino
    robottino.target_position[0] = new_goal_msg.pose.position.x
    robottino.target_position[1] = new_goal_msg.pose.position.y

#Funzione di callback del listener sul topic /tf
#Si occupa di aggiornare i parametri di navigazione del robottino
#sulla base di quanto viene stampato da ROS sul topic
def position_callback(tf):

    #Si accerta di poter effettuare la trasformazione
    transform_ok = transformCalculator.can_transform('map','base_link', rospy.Time(0))

    if transform_ok != 0:

        #Trova i nuovi parametri di navigazione del robottino sulla base della 
        #trasformazione ottenuta con:
        #   -   source_frame = base_link
        #   -   target_frame = map
        #   -   rospy.Time(0) fa si' che i parametri di cui sopra siano gli ultimi disponibili
        transformation = TransformStamped()
        transformation = transformCalculator.lookup_transform('map', 'base_link', rospy.Time(0))
        
        #Aggiorna la posizione del robottino
        robottino.current_position[0] = transformation.transform.translation.x
        robottino.current_position[1] = transformation.transform.translation.y

#Funzione di callback per il timer "timer_arrivato"
#Viene chiamato ogni 0.5 secondi e verifica se il robot e' arrivato a destinazione
def timer_check_status(event = None):

    #Controlla che il robot sia in movimento: altrimenti continuerebbe a pubblicare
    #per tutta la permanenza del robot a destinazione
    if robottino.moving:

        #Check sulla distanza
        if math.sqrt(math.pow(robottino.current_position[0]-robottino.target_position[0], 2)+ 
                     math.pow(robottino.current_position[1]-robottino.target_position[1], 2)) < 1.5:

            if DEBUG: print("Sono arrivato a destinazione")

            #Pubblica "Arrived" sul relativo topic e imposta il valore 0 al parametro moving del robottino
            publisher_check_status.publish("Arrived")
            robottino.moving = False

#Funzione di callback per il timer "timer_incastrato"
#Viene chiamato ogni 6 secondi e verifica se il robot e' rimasto incastrato
def timer_incastrato_check(event = None):

    #Controlla che il robot pensi di essere in movimento: altrimenti continuerebbe a pubblicare
    #per tutta la permanenza del robot a destinazione
    if robottino.moving:

        #Check sulla posizione
        position_x1 = robottino.current_position[0]
        position_y1 = robottino.current_position[1]
        if DEBUG: print("POSIZIONE CORRENTE: [{},{}]".format(position_x1, position_y1))

        sleep(5)

        position_x2 = robottino.current_position[0]
        position_y2 = robottino.current_position[1]
        if DEBUG: print("POSIZIONE CORRENTE: [{},{}]".format(position_x2, position_y2))

        if position_x1 == position_x2 and position_y1 == position_y2:
            
            #Pubblica "Stuck" sul relativo topic e imposta il valore 0 al parametro moving del robottino
            print("Sono bloccato!")
            publisher_check_status.publish('Stuck')
            robottino.moving = False
            
#Inizializza il nodo ROS e le istanze delle classi di cui abbiamo bisogno
#Crea publisher e subscriber in grado di comunicare con i topic ROS
#Continua a ciclare pubblicando la posizione da raggiungere
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

        subscriber_new_goal         = rospy.Subscriber( '/New_Goal',                 NewGoal,        move_to_goal_callback)
        subscriber_tf               = rospy.Subscriber( '/tf',                       TFMessage,      position_callback)

        timer_arrivato              = rospy.Timer(      rospy.Duration(0.5),                         timer_check_status)
        timer_incastrato            = rospy.Timer(      rospy.Duration(6),                           timer_incastrato_check)

        while not rospy.is_shutdown():

            if robottino.info_ricevute:
                publisher_posizione.publish(new_goal_msg)
            
            rate.sleep()

    except rospy.ROSInterruptException:
        pass
