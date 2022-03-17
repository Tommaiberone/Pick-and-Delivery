#include "ros/ros.h"
#include <vector>
#include "geometry_msgs/PoseStamped.h"
#include "tf/tf.h"
#include "tf2_msgs/TFMessage.h"
#include <sstream>
#include <tf2_ros/transform_listener.h>
#include <geometry_msgs/TransformStamped.h>
#include <nav_msgs/Odometry.h>
#include <sensor_msgs/LaserScan.h>

std::vector<float> target_position(2,0);
std::vector<float> old_position(2,0);
std::vector<float> current_position(2,0);

geometry_msgs::PoseStamped new_goal_msg;
tf2_ros::Buffer tfBuffer;

size_t n = 10;
int message_published = 0;
int cruising = 0;
int debug = 0;

void SetGoal_callback(const geometry_msgs::PoseStamped& new_goal)
{
    new_goal_msg.header.seq = n;
    n++;
    new_goal_msg.header.stamp = ros::Time::now();
    new_goal_msg.header.frame_id = "map";
    
    new_goal_msg.pose.position.x = new_goal.pose.position.x;
    new_goal_msg.pose.position.y = new_goal.pose.position.y;
    new_goal_msg.pose.position.z = 0;
    
    new_goal_msg.pose.orientation.x = 0;
    new_goal_msg.pose.orientation.y = 0;
    new_goal_msg.pose.orientation.z = 0;
    new_goal_msg.pose.orientation.w = new_goal.pose.orientation.w;

    message_published = 1;      //Fa sì che la callback viene chiamata solo una volta
    cruising = 1;               //Setta il robot come occupato

    //Save the goal position
    target_position[0] = new_goal_msg.pose.position.x;
    target_position[1] = new_goal_msg.pose.position.y;

    // pub.publish(new_goal_msg);

}

void position_callback (const tf2_msgs::TFMessage& tf)
{
    if (debug)
        ROS_INFO("x position: [%f]", tf.transforms[0].transform.translation.x);

    int transform_ok;
    transform_ok = tfBuffer.canTransform("map", "base_link", ros::Time(0));

    if (debug)
        ROS_INFO("transform possible: [%i]", transform_ok);
    
    if (transform_ok != 0)
    {
        geometry_msgs::TransformStamped transformStamped;
        transformStamped = tfBuffer.lookupTransform("map", "base_link", ros::Time(0));

        if (debug) {
            ROS_INFO("position x, [%f]", transformStamped.transform.translation.x);
            ROS_INFO("position y, [%f]", transformStamped.transform.translation.y);
            ROS_INFO("orientation w, [%f]", transformStamped.transform.rotation.w);
        }

        current_position[0] = transformStamped.transform.translation.x;
        current_position[1] = transformStamped.transform.translation.y;
    }

    
}

void check1_callback(const ros::TimerEvent& event)
{
    if (cruising!=0) {
        ROS_INFO("Check if I'm moving");
        float distance_made, distance_from_target;
        distance_made = sqrt(pow(current_position[0]-old_position[0], 2) +  pow(current_position[1]-old_position[1], 2));
        distance_from_target = sqrt(pow(current_position[0]-target_position[0], 2) +  pow(current_position[1]-target_position[1], 2));

        if (distance_made < 0.8)
        {
            ROS_INFO("I'm stuck!");
        }
        if (distance_from_target < 1.5) 
        {
            ROS_INFO("Arrived to the goal!");
            cruising = 0;
        }

    }
}

void check2_callback(const ros::TimerEvent& event)
{
    if (cruising!=0) {
        ROS_INFO("Checking if it has been passed too much time...");
        float distance_from_target;
        distance_from_target = sqrt(pow(current_position[0]-target_position[0], 2) +  pow(current_position[1]-target_position[1], 2));

        if (distance_from_target < 1.5) 
        {
            ROS_INFO("TIMEOUT: Goal point could not be reached");
        }

    }
}

int main(int argc, char **argv)
{
    /**
    * The ros::init() function needs to see argc and argv so that it can perform
    * any ROS arguments and name remapping that were provided at the command line.
    * For programmatic remappings you can use a different version of init() which takes
    * remappings directly, but for most command-line programs, passing argc and argv is
    * the easiest way to do it.  The third argument to init() is the name of the node.
    *
    * You must call one of the versions of ros::init() before using any other
    * part of the ROS system.
    */
    ros::init(argc, argv, "Set_Goal");

    /**
    * NodeHandle is the main access point to communications with the ROS system.
    * The first NodeHandle constructed will fully initialize this node, and the last
    * NodeHandle destructed will close down the node.
    */
    ros::NodeHandle n;

    /**
    * The advertise() function is how you tell ROS that you want to
    * publish on a given topic name. This invokes a call to the ROS
    * master node, which keeps a registry of who is publishing and who
    * is subscribing. After this advertise() call is made, the master
    * node will notify anyone who is trying to subscribe to this topic name,
    * and they will in turn negotiate a peer-to-peer connection with this
    * node.  advertise() returns a Publisher object which allows you to
    * publish messages on that topic through a call to publish().  Once
    * all copies of the returned Publisher object are destroyed, the topic
    * will be automatically unadvertised.
    *
    * The second parameter to advertise() is the size of the message queue
    * used for publishing messages.  If messages are published more quickly
    * than we can send them, the number here specifies how many messages to
    * buffer up before throwing some away.
    */
    ros::Publisher pub = n.advertise<geometry_msgs::PoseStamped>("/move_base_simple/goal", 1000);
    
    tf2_ros::TransformListener tfListener(tfBuffer);

    ros::Rate loop_rate(10);

  
    //Initialize the subscribers and set the callback functions
    ros::Subscriber sub = n.subscribe("/move_base_simple/goal", 1000, SetGoal_callback);
    ros::Subscriber sub_tf = n.subscribe("tf", 1000, position_callback);

    //Initialize two timers and set the check callback functions
    ros::Timer timer1 = n.createTimer(ros::Duration(0.5), check1_callback);
    ros::Timer timer2 = n.createTimer(ros::Duration(0.5), check2_callback);

    /**
    * A count of how many messages we have sent. This is used to create
    * a unique string for each message.
    */
    int count = 0;
    while (ros::ok())
    {

        if (message_published != 0) {
            ROS_INFO("Publishing a new goal position");
            pub.publish(new_goal_msg);
            message_published = 0;
        }
            /**
            * This is a message object. You stuff it with data, and then publish it.
            */
            //std_msgs::String msg;

            //std::stringstream ss;
            //ss << "hello world " << count;
            //msg.data = ss.str();

            //ROS_INFO("%s", msg.data.c_str());

            /**
            * The publish() function is how you send messages. The parameter
            * is the message object. The type of this object must agree with the type
            * given as a template parameter to the advertise<>() call, as was done
            * in the constructor above.
            */
            //chatter_pub.publish(msg);

        ros::spinOnce();

        loop_rate.sleep();
        ++count;
    }


    return 0;
}

