/*
 * rosserial Publisher Example
 * Prints "hello world!"
 */

#include <ros.h>

#include <std_msgs/UInt16.h>

ros::NodeHandle  nh;

std_msgs::UInt16 str_msg;
int val;
int pre = 0;
ros::Publisher chatter("chatter", &str_msg);
/*
char hello[] = "Hi";
void messageCb(const std_msgs::UInt16 & msg)
      { 
            str_msg.data = hello;
        if (str_msg.data == msg.data){
        
        
        
        chatter.publish( &str_msg );
          }}
ros::Subscriber<std_msgs::UInt16> sub("status", &messageCb );
*/
void setup()
{ Serial.begin(9600);
  nh.initNode();
  nh.advertise(chatter);
  //nh.subscribe(sub);
}

void loop()
{ val = analogRead(2);
  
  Serial.println(val/10.23);
  val = val*5.75/10.23;
  str_msg.data = val;
  
  
  chatter.publish( &str_msg );
  nh.spinOnce();
  delay(1000);
}
