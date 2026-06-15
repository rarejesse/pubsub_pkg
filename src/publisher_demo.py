#! /usr/bin/env python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float32, Header, ColorRGBA
from geometry_msgs.msg import PointStamped
import numpy as np


class PublisherDemo(Node):
    def __init__(self):
        super().__init__('publisher_demo')
        self.get_logger().info('Publisher demo node started...')

        #Create publishers objects for each message type, the 3rd argument relates to QoS settings, 10 is the default queue size for messages
        self.string_publisher = self.create_publisher(String, 'text_data', 10) 
        self.float_publisher = self.create_publisher(Float32, 'float_data', 10)  
        self.header_publisher = self.create_publisher(Header, 'header_data', 10)
        self.color_publisher = self.create_publisher(ColorRGBA, 'color_data', 10)
        self.point_publisher = self.create_publisher(PointStamped, 'point_data', 10)
        
        #Create timers to call the publisher functions at a fixed rate
        #Timers automatically run in independent threads (they don't block each other or the main thread)
        #The first argument is the timer period in seconds, so (1/5.0) means 5 Hz
        self.timer1 = self.create_timer((1/2.0), self.string_publisher_timer)
        self.timer2 = self.create_timer((1/1.0), self.float_publisher_timer)
        self.timer3 = self.create_timer((1/1.0), self.header_publisher_timer)
        self.timer4 = self.create_timer((1/1.0), self.color_publisher_timer)
        self.timer5 = self.create_timer((1/1.5), self.point_publisher_timer)

    def string_publisher_timer(self):
        msg = String()
        msg.data = 'this is text data from {}'.format(self.get_name())
        self.string_publisher.publish(msg)


    def float_publisher_timer(self):
        msg = Float32()
        msg.data = np.random.uniform(-100.0, 100.0) #random float between -100 and 100
        self.float_publisher.publish(msg)
    

    def header_publisher_timer(self):
        msg = Header()
        msg.stamp = self.get_clock().now().to_msg() #current time as a ROS2 timestamp
        msg.frame_id = 'global' #typically indicates the coordinate frame of reference for the data
        self.header_publisher.publish(msg)


    def color_publisher_timer(self):
        msg = ColorRGBA()
        rgba = np.random.random(4) #4 random RGBA values between 0 and 1
        msg.r = rgba[0]
        msg.g = rgba[1]
        msg.b = rgba[2]
        msg.a = rgba[3]
        self.color_publisher.publish(msg)

    def point_publisher_timer(self):
        msg = PointStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'map'
        msg.point.x = np.random.uniform(-10.0, 10.0)
        msg.point.y = np.random.uniform(-10.0, 10.0)
        msg.point.z = np.random.uniform(-10.0, 10.0)
        self.point_publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    publisher_demo = PublisherDemo()
    rclpy.spin(publisher_demo)
    publisher_demo.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
