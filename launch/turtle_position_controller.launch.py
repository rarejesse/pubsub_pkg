from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition, UnlessCondition

def generate_launch_description(): 
    """
    All launch files need to have this function
    This function must return a LaunchDescription object
    You can add nodes to a LaunchDescription object using the add_action() method
    The DelareLaunchArgument variables define options you can use on the command line when you launch this file
    
    """
    
    turtlesim_node = Node( 
            package='turtlesim',
            executable='turtlesim_node')
    
    turtle_position_control_node = Node(
                package='pubsub_pkg',
                executable='turtle_position_controller.py')

    ld = LaunchDescription()            
    ld.add_action(turtlesim_node)
    ld.add_action(turtle_position_control_node)
    return ld