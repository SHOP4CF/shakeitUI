import sys
import threading

from PyQt5.QtWidgets import QApplication
from shakeit_ui.Main import MainWindow

#ROS2
import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from anyfeeder_interfaces.srv import StandardInput
from shakeit_core.util.shakeit_node import create_client_wait_for_service

class ShakeituiNode(Node):
    def __init__(self):
        super().__init__('shakeit_ui_node')
        self.get_logger().info(f"Initializing {self.get_name()}...")

        self.window = MainWindow()

        self.init_feeder_client = create_client_wait_for_service(
            self, StandardInput, 'anyfeeder_node/init')
        
    def init_anyfeeder(self):
        future = self.init_feeder_client.call_async(StandardInput.Request())
        rclpy.spin_until_future_complete(self, future)
        #self.get_logger().info("Anyfeeder initialized")

    def destroy_node(self) -> bool:
        self.get_logger().info("Closing down")
        self.window.close_application()
        return super().destroy_node()
    
    def hallo(self):
        print("hallo world!")

def main(args=None):
    rclpy.init(args=args)
    print('Hi from shakeit_ui.')
    app = QApplication(sys.argv)
    node = ShakeituiNode()

    try:
        x = threading.Thread(target=rclpy.spin, args=(node, MultiThreadedExecutor()), daemon=True)
        x.start()
        app.exec()
    except KeyboardInterrupt:
        node.get_logger().info(f"Ctrl-C detected, shutting {node.get_name()} down!")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
