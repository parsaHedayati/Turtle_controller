# TurtleSim Controllers

This repository contains various ROS 2 nodes to control the movement of a turtle in the TurtleSim simulator. The nodes showcase different control strategies, including basic motion commands, subscription-based feedback control, and advanced fuzzy logic control.

---

## Features

1. **Draw a Circle**: Moves the turtle in a circular path.
2. **Pose Subscriber**: Logs the turtle's current position to the console.
3. **Turtle Controller**: Controls the turtle's movement based on its position, changing speed and pen color dynamically.
4. **Fuzzy Logic Controller**: Implements a fuzzy logic-based control system for adaptive movement based on the turtle's proximity to simulation boundaries.

---

## Prerequisites
### UBUNTU machine

### Install ROS 2
Ensure you have ROS 2 installed on your system. This repository assumes ROS 2 Humble or later.

### Install Dependencies
Install the required Python libraries:
```bash
pip install numpy scikit-fuzzy

```
## Getting Started
1. **clone to the repository:**
2. ```bash
    git clone https://github.com/parsaHedayati/Turtle_controller/edit/master/README.md

```
3. **Launch the TurtleSim Simulator:**
```bash
ros2 run turtlesim turtulesim_node

```
3. **run different nodes, for Example:**
```bash
ros2 run my_robot_controller fuzzy_controller

```

## Fuzzy Logic System Details

### Inputs
- **Proximity**: Distance to the nearest boundary.

### Outputs
- **Linear Velocity**: Speed of forward movement.
- **Angular Velocity**: Turning rate.

### Fuzzy Membership Functions

#### Proximity
- Near
- Medium
- Far

#### Linear Velocity
- Slow
- Medium
- Fast

#### Angular Velocity
- Left
- None
- Right

### Rules
1. If proximity is **near**, then turn **left** and move **slow**.
2. If proximity is **medium**, then turn **none** and move **medium**.
3. If proximity is **far**, then turn **none** and move **fast**.


