#! /usr/bin/env python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float32, Header, ColorRGBA
from geometry_msgs.msg import Twist
import numpy as np
from turtlesim.srv import TeleportAbsolute, Spawn
from turtlesim.msg import Pose




class TurtlePositionController(Node):
    def __init__(self):
        super().__init__('turtle_position_controller')
        self.get_logger().info('Turtle Position Controller node started...')


        # First set the reference turtle (turtle1) to some starting position
        self.teleport_client = self.create_client(TeleportAbsolute, 'turtle1/teleport_absolute')
        self.teleport_req = TeleportAbsolute.Request(x=5.5, y=5.5, theta=np.pi/2) #define the request to teleport the turtle
        while not self.teleport_client.wait_for_service(timeout_sec=1.0): #attempt to call the turtlesim service, or timeout after  1 second
            self.get_logger().info('teleport service not available, waiting again...')

        #teleport the turtle1 to the starting position
        self.teleport_client.call_async(self.teleport_req)
        

        # Then spawn a second turtle (turtle2) at a different position
        self.spawn_client = self.create_client(Spawn, 'spawn')
        self.spawn_req = Spawn.Request(x=4.5, y=5.5, theta=np.pi/2, name='turtle2') #spawn turtle2 at a different position than turtle1
        while not self.spawn_client.wait_for_service(timeout_sec=1.0): #attempt to call the turtlesim service, or timeout after  1 second
            self.get_logger().info('spawn service not available, waiting again...')
        #spawn the turtle2
        self.spawn_client.call_async(self.spawn_req)


        self.random_teleport_timer = self.create_timer(3.0, self.random_teleport_callback) #create a timer to call the random_teleport function every 5 seconds

        # Create a subscriber to listen to the position of turtle1
        self.reference_position_sub = self.create_subscription(Pose, 'turtle1/pose', self.reference_position_callback, 10)
        self.position_sub = self.create_subscription(Pose, 'turtle2/pose', self.position_callback, 10) #subscribe to turtle2's position so we can get its current position

        #Create a publisher for turtle2's command velocity
        self.cmd_vel_publisher = self.create_publisher(Twist, 'turtle2/cmd_vel', 10)    

        self.control_timer = self.create_timer(0.2, self.control_callback) #create a timer to call the control function every 0.2 seconds (5 Hz)


        #Make some local variables to store the state of turtle1 and turtle2 (this is only 1DOF up and down motion, so we only need one position variable for each)
        self.reference_y = 0.0 #to hold the turtle1 position (the reference position)
        self.y = 0.0 #to hold the turtle2 position 

        #Set the PID gains
        self.gain_p = 2.0
        self.gain_i = 0.0
        self.gain_d = 0.0
        self.error = 0.0



    def reference_position_callback(self, msg):
        # When we receive the position of turtle1, we will teleport turtle2 to the same position
        self.reference_y = msg.y #store the reference position of turtle1

    def position_callback(self, msg):
        # When we receive the position of turtle2, we will store it in a local variable
        self.y = msg.y #store the current position of turtle2

    def random_teleport_callback(self):
        # This function randomly teleports turtle1 to a new position in the turtlesim window
        #choose a random integer between 2 and 9 to set as the reference turtle's y-position
        setpoint = np.random.randint(2, 10)
        self.teleport_req.y = float(setpoint)
        self.teleport_client.call_async(self.teleport_req)

    def control_callback(self):
        #=======================================ADD YOUR CODE HERE=========================================
        #Implement a PID controller (or simply a P-controller) to control turtle2's position based on turtle1's position

       
        pass



def main(args=None):
    rclpy.init(args=args)
    turtle_position_controller = TurtlePositionController()
    rclpy.spin(turtle_position_controller)
    turtle_position_controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
