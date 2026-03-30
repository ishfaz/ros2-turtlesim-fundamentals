# ROS2 Turtle Hunter 🐢

A ROS2 project built on top of turtlesim where turtle1 autonomously hunts and catches randomly spawning turtles. Built as a hands-on introduction to core ROS2 concepts — topics, services, custom messages, parameters, and launch files.

---

## Demo

<video src="https://github.com/Ishfaz/ros2-turtlesim-fundamentals/raw/main/turtle.webm" controls width="800"></video>

---

## What it does

- Turtles spawn at random positions every few seconds
- Turtle1 automatically calculates the nearest turtle and chases it
- When caught, the turtle is killed and the score updates
- Turtle1's pen changes to a random color after each catch
- A live score window shows your progress
- Game ends when you reach the target number of catches

---

## Workspace Structure

```
turtlesim_ws/
└── src/
    ├── turtle_msgs/          # Custom ROS2 message and service definitions
    │   ├── msg/
    │   │   ├── AliveTurtle.msg    # Carries spawned turtle position and name
    │   │   └── KillTurtle.msg     # Carries the name of turtle to kill
    │   └── srv/
    │       └── ComputeRectangleArea.srv  # length + width → area
    │
    ├── turtle_script/        # All Python nodes
    │   └── turtle_script/
    │       ├── draw_circle.py          # Draws turtle in a circle (open loop)
    │       ├── Polygon_drawer.py       # Draws any polygon using pose feedback (closed loop)
    │       ├── area_service_server.py  # Service server: computes rectangle area
    │       ├── area_service_client.py  # Service client: sends length/width, receives area
    │       ├── turtle_spawner.py       # Spawns turtles randomly, kills on request
    │       ├── turtle_controller.py    # Chases nearest turtle, tracks score
    │       └── score_display.py       # Live score window using tkinter
    │
    └── turtle_bringup/       # Launch files
        └── launch/
            ├── Kill_them_all.launch.py  # Main game launcher
            └── Polygon.launch.py        # Polygon drawer launcher
```

---

## ROS2 Concepts Covered

| Concept | Where used |
|---|---|
| Topics (publish/subscribe) | cmd_vel, pose, turtle_alive, turtle_kill, turtle_score |
| Services (request/response) | spawn, kill, compute_area, set_pen |
| Custom messages | AliveTurtle.msg, KillTurtle.msg |
| Custom services | ComputeRectangleArea.srv |
| Parameters | difficulty, speed, max_catches, sides, side_length |
| Launch files | Kill_them_all.launch.py, Polygon.launch.py |
| Closed loop control | Polygon_drawer.py, turtle_controller.py |
| State machine | Polygon_drawer.py |

---

## Node Communication Graph

```
turtle_spawner_node
    │── publishes  →  /turtle_alive     →  turtle_controller_node
    │── subscribes ←  /turtle_kill      ←  turtle_controller_node
    │── calls      →  /spawn service    →  turtlesim
    └── calls      →  /kill service     →  turtlesim

turtle_controller_node
    │── publishes  →  /turtle1/cmd_vel  →  turtlesim
    │── subscribes ←  /turtle1/pose     ←  turtlesim
    │── publishes  →  /turtle_score     →  score_display_node
    └── calls      →  /turtle1/set_pen  →  turtlesim

score_display_node
    └── subscribes ←  /turtle_score     ←  turtle_controller_node
```

---

## Requirements

- ROS2 Humble
- Python 3.10+
- turtlesim: `sudo apt install ros-humble-turtlesim`
- tkinter: `sudo apt install python3-tk`

---

## Build

```bash
cd ~/turtlesim_ws
colcon build
source install/setup.bash
```

---

## Run the Game

The main launch file `Kill_them_all.launch.py` starts **4 nodes at once**:
- `turtlesim_node` — the simulation window
- `turtle_spawner` — spawns turtles randomly
- `turtle_controller` — chases and catches turtles
- `score_display` — live score window

**Default settings (medium difficulty, 10 catches):**
```bash
ros2 launch turtle_bringup Kill_them_all.launch.py
```

**Easy — slow spawn, slow turtle:**
```bash
ros2 launch turtle_bringup Kill_them_all.launch.py difficulty:=easy speed:=1.0 max_catches:=5
```

**Hard — fast spawn, fast turtle:**
```bash
ros2 launch turtle_bringup Kill_them_all.launch.py difficulty:=hard speed:=4.0 max_catches:=20
```

| Parameter | Options | Default | Effect |
|---|---|---|---|
| `difficulty` | easy / medium / hard | medium | spawn rate (3s / 1.5s / 0.5s) |
| `speed` | any float | 2.0 | how fast turtle1 chases |
| `max_catches` | any int | 10 | game ends after this many catches |

---

## Run Polygon Drawer

The second launch file `Polygon.launch.py` starts turtlesim and draws a polygon:

```bash
ros2 launch turtle_bringup Polygon.launch.py
```

Or with custom shape:
```bash
ros2 launch turtle_bringup Polygon.launch.py sides:=6 side_length:=2.0
```

| Parameter | Default | Effect |
|---|---|---|
| `sides` | 3 | number of sides (3=triangle, 4=square, 6=hexagon) |
| `side_length` | 2.0 | length of each side |

---

## Run Individual Nodes

**Draw a circle:**
```bash
ros2 run turtlesim turtlesim_node
ros2 run turtle_script draw_circle
```

**Draw a polygon:**
```bash
ros2 run turtlesim turtlesim_node
ros2 run turtle_script Polygon_drawer --ros-args -p sides:=6 -p side_length:=2.0
```

**Area service:**
```bash
ros2 run turtle_script area_service_server
ros2 run turtle_script area_service_client --ros-args -p length:=7.0 -p width:=4.0
```