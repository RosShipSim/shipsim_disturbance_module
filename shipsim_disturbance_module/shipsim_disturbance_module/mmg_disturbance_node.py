#! /usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np

import rclpy
from rclpy.node import Node

from shipsim_msgs_module.msg import Disturbance

class MmgDisturbanceNode(Node):
    """DisturbanceNode."""

    disturbance = Disturbance()

    def __init__(self):
        """init."""
        super().__init__("disturbance", namespace="ship1")
        self.declare_parameter("publish_address", "/ship1/disturbance")
        self.declare_parameter("delta_time", 0.005)

        # Disturbance
        self.declare_parameter("mu_X_D_0", 10.0)
        self.declare_parameter("sigma_X_D_0", 3.0)
        self.declare_parameter("mu_Y_D_0", 10.0)
        self.declare_parameter("sigma_Y_D_0", 3.0)

        publish_address = (
            self.get_parameter("publish_address").get_parameter_value().string_value
        )
        self.pub_disturbance = self.create_publisher(Disturbance, publish_address, 10)

        delta_time = self.get_parameter("delta_time").value
        self.timer = self.create_timer(delta_time, self.sender_callback)

    def sender_callback(self):
        """sender_callback."""

        # 外乱
        mu_X_D_0 = self.get_parameter("mu_X_D_0").value
        sigma_X_D_0 = self.get_parameter("sigma_X_D_0").value
        mu_Y_D_0 = self.get_parameter("mu_Y_D_0").value
        sigma_Y_D_0 = self.get_parameter("sigma_Y_D_0").value

        # 外乱の設定と座標変換
        X_D_0 = np.random.normal(
            mu_X_D_0, sigma_X_D_0
        )
        Y_D_0 = np.random.normal(
            mu_Y_D_0, sigma_Y_D_0
        )

        self.disturbance.x_d_0 = X_D_0
        self.disturbance.y_d_0 = Y_D_0

        self.pub_disturbance.publish(self.disturbance)
        self.get_logger().info(
            'Disturbance Publishing: "%s","%s" '
            % (
                self.disturbance.x_d_0,
                self.disturbance.y_d_0,
            )
        )

def main(args=None):
    """Run main."""
    rclpy.init(args=args)

    node = MmgDisturbanceNode()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()