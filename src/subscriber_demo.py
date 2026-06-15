#! /usr/bin/env python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float32, Header, ColorRGBA
from geometry_msgs.msg import PointStamped
import numpy as np
import datetime

class SubscriberDemo(Node):
    def __init__(self):
        super().__init__('subscriber_demo')
        self.get_logger().info('Subscriber demo node started...')

        self.string_subscriber = self.create_subscription(String, 'text_data', self.string_callback, 10)
        self.float_subscriber = self.create_subscription(Float32, 'float_data', self.float_callback, 10)
        self.header_subscriber = self.create_subscription(Header, 'header_data', self.header_callback, 10)
        self.color_subscriber = self.create_subscription(ColorRGBA, 'color_data', self.color_callback, 10)
        self.point_subscriber = self.create_subscription(PointStamped, 'point_data', self.point_callback, 10)

    def string_callback(self, msg):
        self.get_logger().info('Received string: "{}" \n'.format(msg.data), throttle_duration_sec=1.0) #throttle_duration_sec limits how often the message is printed to the console (1 message per second in this case)

    def float_callback(self, msg):
        sign = ['NEGATIVE', 'POSITIVE'][int(msg.data > 0)]
        self.get_logger().info('Received {} float value: {:.3f} \n'.format(sign, msg.data))

    def header_callback(self, msg):
        #Convert the received timestamp to a human-readable format YYYY.MM.DD HH:MM:SS.ssssss
        timestamp = msg.stamp.sec + msg.stamp.nanosec / 1e9
        time_str = datetime.datetime.fromtimestamp(timestamp).strftime('%Y.%m.%d %H:%M:%S.%f')
        self.get_logger().info('Received header with timestamp: {} and frame_id: {} \n'.format(time_str, msg.frame_id))

    def color_callback(self, msg):
        self.get_logger().info('Received color r: {:.2f}, g: {:.2f}, b: {:.2f}, a: {:.2f} \n'.format(msg.r, msg.g, msg.b, msg.a))

    def point_callback(self, msg):
        self.get_logger().info('Received 3D point: [{:.2f}, {:.2f}, {:.2f}] \n'.format(msg.point.x, msg.point.y, msg.point.z))

def main(args=None):
    rclpy.init(args=args)
    subscriber_demo = SubscriberDemo()
    rclpy.spin(subscriber_demo)
    subscriber_demo.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
