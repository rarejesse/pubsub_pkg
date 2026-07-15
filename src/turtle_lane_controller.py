#! /usr/bin/env python3
import rclpy
from rclpy.node import Node

import time 
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import random
from turtlesim.srv import Spawn, TeleportAbsolute, Kill, SetPen
import colorsys


class TurtleController(Node):
    def __init__(self):
        super().__init__('turtle_controller')
        self.velocity_publisher = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)
        self.pose_subscriber = self.create_subscription(Pose, 'turtle1/pose', self.pose_callback, 10)
        
        #publishers for turtle2 and turtle3 to draw the lane
        self.velocity_publisher2 = self.create_publisher(Twist, 'turtle2/cmd_vel', 10)
        self.velocity_publisher3 = self.create_publisher(Twist, 'turtle3/cmd_vel', 10)
        self.lane_width = 2.0 
        self.speed = 2.0  # Forward speed: assume it must remain constant the whole time
        self.velocity = Twist()
        self.velocity.linear.x = self.speed
        self.position_error = 0.0
        self.position_error_integral = 0.0
        self.position_error_prev = 0.0
        self.position_error_rate = 0.0
        self.heading_error = 0.0


        #Set the PID gains: TODO: Make these ROS2 parameters that can be set from a yaml file
        self.gain_p = 2.0
        self.gain_i = 0.0
        self.gain_d = 0.0
        
        self.timer_period = 0.1  # seconds
        self.timer = self.create_timer(self.timer_period, self.controller_callback)

    def random_initialize_turtle(self):
        angle1 = random.uniform(0.6*math.pi, 0.8*math.pi)
        angle2 = random.uniform(0.2*math.pi, 0.4*math.pi)
        self.spawn_turtle('turtle1', 5.5, 0.5, random.choice([angle1, angle2]))
        time.sleep(0.25)
        random_color = colorsys.hsv_to_rgb(random.random(), 1.0, 1.0) 
        random_color = [int(255*c) for c in random_color]
        self.set_pen('turtle1', *random_color, 3,False)

    def set_pen(self, name, r, g, b, width, off):
        client = self.create_client(SetPen, '{}/set_pen'.format(name))
        while not client.wait_for_service(timeout_sec=3.0):
            self.get_logger().info('Waiting for set_pen service...')
        request = SetPen.Request()
        request.r = r
        request.g = g
        request.b = b
        request.width = width
        request.off = off
        response = client.call_async(request)
        if response is not None:
            self.get_logger().info('Successfully set pen for {}'.format(name))
        else:
            self.get_logger().error('Failed to set pen for {}'.format(name))
        
    def spawn_turtle(self, name, x, y, theta):
        client = self.create_client(Spawn, 'spawn')
        while not client.wait_for_service(timeout_sec=3.0):
            self.get_logger().info('Waiting for spawn service...')
        request = Spawn.Request(x=x, y=y, theta=theta, name=name)
        response = client.call_async(request)
        if response is not None:
            self.get_logger().info('Successfully spawned {}'.format(name))
        else:
            self.get_logger().error('Failed to spawn {}'.format(name))

    def kill_turtle(self, name):
        client = self.create_client(Kill, 'kill')
        while not client.wait_for_service(timeout_sec=3.0):
            self.get_logger().info('Waiting for kill service...')
        request = Kill.Request()
        request.name = name
        response = client.call_async(request)
        if response is not None:
            self.get_logger().info('Successfully killed {}'.format(name))
        else:
            self.get_logger().error('Failed to kill {}'.format(name))

    def draw_lanes(self):
        vel = Twist()
        vel.linear.x = 5.0

        sleep_rate = self.create_rate(1.0)
        for _ in range(3):
            self.velocity_publisher2.publish(vel)
            self.velocity_publisher3.publish(vel)
            print("Drawing lanes...")
            time.sleep(1.0)
        self.kill_turtle('turtle2')
        self.kill_turtle('turtle3')

    def controller_callback(self):
        #==========================================================================================================================
        #RULES: The forward speed (self.velocity.linear.x) must remain constant the whole time (the value of self.speed)
        #       The lateral speed (self.velocity.linear.y) must remain zero the whole time

        #PID controller
        self.velocity.angular.z = self.gain_p*self.position_error + self.gain_i*self.position_error_integral + self.gain_d*self.position_error_rate
        self.velocity_publisher.publish(self.velocity)

    def pose_callback(self, msg):
        self.x = msg.x
        self.y = msg.y
        self.theta = msg.theta
        self.position_error_prev = self.position_error
        self.position_error = (self.x-5.5) #Center of lane is at x=5.5
        self.position_error_integral += self.position_error * self.timer_period
        self.heading_ref = 0.2*self.position_error- math.radians(90)
        self.heading_error = self.theta - self.heading_ref
        self.position_error_rate = (self.position_error-self.position_error_prev) / self.timer_period
        if abs(self.position_error) > self.lane_width/2:
            self.get_logger().warn('TURTLE OUT OF BOUNDS! Position error: {:.2f}'.format(self.position_error), throttle_duration_sec=0.5)
        if abs(self.position_error) > 4.0 or self.y > 10.5:
            self.kill_turtle('turtle1') #Kill and respawn turtle if it goes too far out of bounds
            time.sleep(0.25)
            self.random_initialize_turtle()
        self.get_logger().info('Position error: {:.2f}'.format(self.position_error), throttle_duration_sec=0.5)

def main(args=None):
    rclpy.init(args=args)

    turtle_controller = TurtleController()
    turtle_controller.kill_turtle('turtle1')
        
    # Spawn turtle2 and turtle3 to draw the 'lane'
    left_boundary = 5.5 - turtle_controller.lane_width/2
    right_boundary = 5.5 + turtle_controller.lane_width/2
    turtle_controller.spawn_turtle('turtle2', left_boundary, 0.5, math.radians(90.0))
    turtle_controller.spawn_turtle('turtle3', right_boundary, 0.5, math.radians(90.0))
    turtle_controller.draw_lanes()


    turtle_controller.random_initialize_turtle()
    rclpy.spin(turtle_controller)
    turtle_controller.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

