import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit
from shakeit_ui.MainUI import Ui_MainWindow
from shakeit_ui.Interaction import InteractionWindow
from shakeit_ui.KeyrockAPI import KeyrockAPI

#ROS 2
import rclpy
from rclpy import Future
from rclpy.node import Node
from rclpy.action.server import ServerGoalHandle
from shakeit_interfaces.action import FreeObjects, Trigger
from shakeit_interfaces.action import Pick
from shakeit_core.util import create_action_client_wait_for_server, create_client_wait_for_service
from action_msgs.msg import GoalStatus
from anyfeeder_interfaces.srv import StandardInput


class MainWindow:
    def __init__(self, node: Node):
        # setting up ros2 stuff #
        self.node = node
        # TODO: Maybe look into service names, remap names in launch file
        # Se control_node remapping from shakeit_core
        self.init_feeder_client = create_client_wait_for_service(
            self.node, StandardInput, 'feeder/init')
        self.add_objects_client = create_client_wait_for_service(
            self.node, StandardInput, 'feeder/add')
        self.purge_objects_client = create_client_wait_for_service(
            self.node, StandardInput, 'feeder/purge')
        self.flip_objects_client = create_client_wait_for_service(
            self.node, StandardInput, 'feeder/flip')
        self.forward_objects_client = create_client_wait_for_service(
            self.node, StandardInput, 'feeder/forward')
        self.backward_objects_client = create_client_wait_for_service(
            self.node, StandardInput, 'feeder/backward')

        self.pick_action_client = create_action_client_wait_for_server(
            self.node, Pick, 'kuka_adapter/pick')
        self.free_objects_client = create_action_client_wait_for_server(
            self.node, FreeObjects, 'sensopart_adapter/free_objects')

        # setting up keyrock #
        self.keyrockAPI = KeyrockAPI()

        # setting up UI #
        self.main_win = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_win)

        self.ui.stackedLogin.setCurrentWidget(self.ui.loginPage)  # setting the starting widget
        self.ui.textPassword.setEchoMode(QLineEdit.Password)
        self.ui.labelLoginError.hide()

        # set up UI for interaction component
        self.interactionui = InteractionWindow(self)
        self.ui.stackedLogin.addWidget(self.interactionui.getWidget())

        # connecting buttons
        self.ui.buttonLogin.clicked.connect(self.login)
        self.ui.buttonLogout.clicked.connect(self.logout)

        # connecting radiobuttons
        self.ui.radioAI.toggled.connect(self.ai)
        self.ui.radioManual.toggled.connect(self.manual)
        self.ui.radioBoard.toggled.connect(self.leaderboard)
        self.ui.radioInteraction.toggled.connect(self.startInteraction)

        self.init_anyfeeder()

        self.show()

    def login(self):
        username = self.ui.textUsername.text()
        password = self.ui.textPassword.text()

        # # authenticate user using keyrock
        # result, accessToken = self.keyrockAPI.authenticateUser(username, password)

        # if result:
        #     # success
        #     userInfo = self.keyrockAPI.getUserInfo(accessToken)

        #     try:
        #         self.ui.labelRole.setText(userInfo['roles'][0]['name'])
        #     except:
        #         self.ui.labelRole.setText("")

        #     self.ui.labelUsername_2.setText(userInfo['username'])

        # change to mainPage
        self.ui.stackedLogin.setCurrentWidget(self.ui.mainPage)
        self.ui.stackedPages.setCurrentWidget(self.ui.pageAI)
        self.ui.radioAI.toggle()

        #     # clear the login page
        #     self.ui.textPassword.clear()
        #     self.ui.textUsername.clear()
        #     self.ui.labelLoginError.hide()

        # else:
        #     # failure
        #     self.ui.labelLoginError.show()
        #     self.ui.textPassword.clear()
        #     self.ui.textUsername.clear()

    def logout(self):
        self.ui.stackedLogin.setCurrentWidget(self.ui.loginPage)

    def ai(self):
        self.ui.stackedPages.setCurrentWidget(self.ui.pageAI)

    def manual(self):
        self.ui.stackedPages.setCurrentWidget(self.ui.pageManual)

    def leaderboard(self):
        self.ui.stackedPages.setCurrentWidget(self.ui.pageBoard)

    def updateLeaderboard(self, players):
        for i, p in enumerate(players):
            if i > 9:
                break
            exec("self.ui.name{}.setText(p['name'])".format(i+1))
            exec("self.ui.pickups{}.setText('{} pickups')".format(i+1, p['score']))

    def startInteraction(self):
        self.ui.stackedLogin.setCurrentWidget(self.interactionui.getWidget())
        self.interactionui.startup()

    def endInteraction(self):
        self.ui.radioBoard.toggle()
        self.ui.stackedLogin.setCurrentWidget(self.ui.mainPage)
        self.leaderboard()

    def show(self):
        self.main_win.show()

    def init_anyfeeder(self):
        future = self.init_feeder_client.call_async(StandardInput.Request())
        rclpy.spin_until_future_complete(self.node, future)
        self.node.get_logger().info("Anyfeeder initialized")

    def add_objects(self):
        request = StandardInput.Request()
        request.parameters.repetitions = 5
        request.parameters.speed = 6
        future = self.add_objects_client.call_async(request)
        rclpy.spin_until_future_complete(self.node, future)
        self.node.get_logger().info("Objects added")

    def forward_objects(self, repetitions, speed):
        request = StandardInput.Request()
        request.parameters.repetitions = repetitions
        request.parameters.speed = speed
        future = self.forward_objects_client.call_async(request)
        rclpy.spin_until_future_complete(self.node, future)
        self.node.get_logger().info("Objects feed forward")

    def flip_objects(self, repetitions, speed):
        request = StandardInput.Request()
        request.parameters.repetitions = repetitions
        request.parameters.speed = speed
        future = self.flip_objects_client.call_async(request)
        rclpy.spin_until_future_complete(self.node, future)
        self.node.get_logger().info("Objects flipped")

    def backward_objects(self, repetitions, speed):
        request = StandardInput.Request()
        request.parameters.repetitions = repetitions
        request.parameters.speed = speed
        future = self.backward_objects_client.call_async(request)
        rclpy.spin_until_future_complete(self.node, future)
        self.node.get_logger().info("Objects feed backward")

    def purge_objects(self):
        future = self.purge_objects_client.call_async(StandardInput.Request())
        rclpy.spin_until_future_complete(self.node, future)
        self.node.get_logger().info("Objects purged")

    def execute_callback(self):
        self.node.get_logger().info(f"Executing goal...")
        result = Trigger.Result()
        result.success = False

        print("Line 186")

        res = self.free_objects_client.send_goal(FreeObjects.Goal())
        print("line 189")
        if res.status != GoalStatus.STATUS_SUCCEEDED:
            msg = f"[GET_FREE_OBJECTS] Response: {res}"
            self.node.get_logger().error(msg)
            result.message = msg
            return result
        free_objects: FreeObjects.Result = res.result
        if free_objects.count == 0:
            result.message = "No objects to pick!"
            return result

        pick_pose = free_objects.poses[0]
        
        goal = Pick.Goal()
        goal.pose = pick_pose
        res = self.pick_action_client.send_goal(goal, feedback_callback=self.feedback_callback)

        # TODO: Call pickupSuccess from interaction see munal_node for if statement
        response: Pick.Result = res.result
        if res.status == GoalStatus.STATUS_SUCCEEDED:
            self.interactionui.pickupSuccess()
        result.success = response.success
        result.message = response.message
        return result

    def feedback_callback(self, feedback):
        self.node.get_logger().info(f"Received feedback: {feedback.feedback.message}")

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     main_win = MainWindow()
#     main_win.show()
#     sys.exit(app.exec_())
