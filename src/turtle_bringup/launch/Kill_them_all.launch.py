from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    ld = LaunchDescription()

    # Declare arguments passable from terminal
    difficulty_arg = DeclareLaunchArgument("difficulty", default_value="medium")
    speed_arg = DeclareLaunchArgument("speed", default_value="2.0")
    max_catches_arg = DeclareLaunchArgument("max_catches", default_value="10")

    turtlesim_node = Node(
        package = "turtlesim",
        executable = "turtlesim_node",
    )

    turtle_controller_node = Node(
        package = "turtle_script",
        executable = "turtle_controller",
        parameters = [
            {"speed": LaunchConfiguration("speed")},
            {"max_catches": LaunchConfiguration("max_catches")},
        ],
        output = "screen"
    )

    turtle_spawner_node = Node(
        package = "turtle_script",
        executable = "turtle_spawner",
        parameters = [
            {"difficulty": LaunchConfiguration("difficulty")},
        ],
        output = "screen"
    )

    score_display_node = Node(
        package = "turtle_script",
        executable = "score_display",
        parameters = [
            {"max_catches": LaunchConfiguration("max_catches")},
            {"difficulty": LaunchConfiguration("difficulty")},
        ],
        output = "screen"
    )

    ld.add_action(difficulty_arg)
    ld.add_action(speed_arg)
    ld.add_action(max_catches_arg)
    ld.add_action(turtlesim_node)
    ld.add_action(turtle_controller_node)
    ld.add_action(turtle_spawner_node)
    ld.add_action(score_display_node)

    return ld