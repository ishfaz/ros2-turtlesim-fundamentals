# turtlesim_ws

## Workspace structure

```
src/
├── turtle_msgs/        ← ament_cmake  — custom .srv and .msg interfaces
├── turtle_script/      ← ament_python — Python nodes
└── turtle_bringup/     ← ament_cmake  — launch files
```

## Packages

### turtle_msgs
- `srv/ComputeRectangleArea.srv` — custom service: length + width → area
- Any new .srv or .msg must be registered in `CMakeLists.txt` under `rosidl_generate_interfaces`

### turtle_script
Nodes:
- `draw_circle.py` — draws a circle using open loop velocity commands
- `Polygon_drawer.py` — draws a closed loop polygon using pose feedback, accepts `sides` and `side_length` parameters
- `area_service_server.py` — service server that computes rectangle area
- `area_service_client.py` — service client that calls the area server
- `turtle_spawner.py` — spawns and kills turtles using turtlesim services
- `turtle_controller.py` — controls turtle movement

### turtle_bringup
- Contains launch files in `launch/` folder
- Launch files are written in Python but package uses `ament_cmake`

## Build and source

```bash
cd ~/turtlesim_ws
colcon build
source install/setup.bash
```

## Run nodes

```bash
# Start turtlesim
ros2 run turtlesim turtlesim_node

# Draw circle
ros2 run turtle_script draw_circle

# Draw polygon with parameters
ros2 run turtle_script polygon_drawer --ros-args -p sides:=6 -p side_length:=2.0

# Area service
ros2 run turtle_script area_service_server
ros2 run turtle_script area_service_client --ros-args -p length:=7.0 -p width:=4.0
```

## Run launch file

```bash
ros2 launch turtle_bringup start_all.launch.py
```

## Key rules
- Only `declare_parameter()` values can be passed from terminal via `--ros-args -p`
- ROS2 dependencies go in `package.xml`, Python pip libraries go in `setup.py`
- Every new node must be registered in `setup.py` entry_points
- Every new .srv/.msg must be registered in `CMakeLists.txt`
- Always rebuild after changing `setup.py` or `CMakeLists.txt`
