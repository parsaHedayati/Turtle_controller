#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from turtlesim.srv import SetPen
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class TurtleFuzzyControllerNode(Node):
    def __init__(self):
        super().__init__("turtle_fuzzy_controller")
        self.previous_x = 0
        self.cmd_vel_publisher_ = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.pose_subscriber = self.create_subscription(Pose, "/turtle1/pose", self.pose_callback, 10)
        
        
        self.proximity = ctrl.Antecedent(np.arange(0, 11, 0.1), 'proximity')
        self.angular_velocity = ctrl.Consequent(np.arange(-2, 2.1, 0.1), 'angular_velocity')
        self.linear_velocity = ctrl.Consequent(np.arange(0, 6, 0.1), 'linear_velocity')

        
        self.proximity['near'] = fuzz.trapmf(self.proximity.universe, [0, 0, 2, 4])
        self.proximity['medium'] = fuzz.trimf(self.proximity.universe, [2, 5, 8])
        self.proximity['far'] = fuzz.trapmf(self.proximity.universe, [6, 8, 10, 10])

        self.angular_velocity['left'] = fuzz.trimf(self.angular_velocity.universe, [-2, -1, 0])
        self.angular_velocity['none'] = fuzz.trimf(self.angular_velocity.universe, [-0.5, 0, 0.5])
        self.angular_velocity['right'] = fuzz.trimf(self.angular_velocity.universe, [0, 1, 2])

        self.linear_velocity['slow'] = fuzz.trimf(self.linear_velocity.universe, [0, 1, 3])
        self.linear_velocity['medium'] = fuzz.trimf(self.linear_velocity.universe, [2, 4, 5])
        self.linear_velocity['fast'] = fuzz.trimf(self.linear_velocity.universe, [4, 5, 6])

        
        rule1 = ctrl.Rule(self.proximity['near'], (self.angular_velocity['left'], self.linear_velocity['slow']))
        rule2 = ctrl.Rule(self.proximity['medium'], (self.angular_velocity['none'], self.linear_velocity['medium']))
        rule3 = ctrl.Rule(self.proximity['far'], (self.angular_velocity['none'], self.linear_velocity['fast']))

        
        self.control_system = ctrl.ControlSystem([rule1, rule2, rule3])
        self.simulator = ctrl.ControlSystemSimulation(self.control_system)

        self.get_logger().info("Turtle Fuzzy Controller Node has been started!")

    def pose_callback(self, pose: Pose):
        
        proximity_to_boundary = min(pose.x, 11 - pose.x, pose.y, 11 - pose.y)

        
        self.simulator.input['proximity'] = proximity_to_boundary

        
        self.simulator.compute()
        linear_velocity = self.simulator.output['linear_velocity']
        angular_velocity = self.simulator.output['angular_velocity']

        
        self.get_logger().info(f"Proximity: {proximity_to_boundary:.2f}, Linear Velocity: {linear_velocity:.2f}, Angular Velocity: {angular_velocity:.2f}")

        
        cmd = Twist()
        cmd.linear.x = linear_velocity
        cmd.angular.z = angular_velocity
        self.cmd_vel_publisher_.publish(cmd)

def main(args=None):
    rclpy.init(args=args)
    node = TurtleFuzzyControllerNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
