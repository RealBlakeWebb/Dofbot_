from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
import os

def generate_launch_description():
    urdf_file_path = os.path.expanduser('~/Documents/Dofbot/dofbot.urdf')

    if not os.path.exists(urdf_file_path):
        raise FileNotFoundError(f"URDF file not found: {urdf_file_path}")

    with open(urdf_file_path, 'r') as urdf_file:
        urdf_content = urdf_file.read()

    return LaunchDescription([
        # Start Gazebo server
        ExecuteProcess(
            cmd=['gzserver', '--verbose', '-s', 'libgazebo_ros_factory.so'],
            output='screen'
        ),
        # Robot state publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'dofbot_description': urdf_content}]
        ),
        # Spawn the entity in Gazebo
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=['-topic', 'dofbot_description', '-entity', 'my_robot'],
            output='screen'
        ),
        # RViz2 for visualization
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', os.path.expanduser('~/Documents/Dofbot/config.rviz')]
        ),
    ])
