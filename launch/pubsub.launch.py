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
    enable_subscriber = DeclareLaunchArgument(name='enable_subscriber',  
                                      default_value='true',   
                                      description='enable the subscriber node')
    
    
    node1 = Node( 
            package='pubsub_pkg',
            executable='publisher_demo.py')
    
    node2 = Node( 
            condition=IfCondition(LaunchConfiguration('enable_subscriber')),
            package='pubsub_pkg',
            executable='subscriber_demo.py')

    ld = LaunchDescription()            
    ld.add_action(enable_subscriber)
    ld.add_action(node1)
    ld.add_action(node2)
    return ld