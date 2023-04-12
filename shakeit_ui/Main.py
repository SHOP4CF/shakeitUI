import sys
from threading import Timer, Thread

from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit
from shakeit_ui.MainUI import Ui_MainWindow
from shakeit_ui.Interaction import InteractionWindow
from shakeit_ui.KeyrockAPI import KeyrockAPI
from shakeit_ui.User import LoggedInUser

#ROS 2
import rclpy
from rclpy import Future
from rclpy.node import Node
from rclpy.action import ActionClient
from shakeit_interfaces.action import FreeObjects, Trigger
from shakeit_core.util import create_action_client_wait_for_server, create_client_wait_for_service
from action_msgs.msg import GoalStatus
from anyfeeder_interfaces.srv import StandardInput

from action_tutorials_interfaces.action import Fibonacci

def endAccessTime(api, user, mainwin):
    newUser = api.refreshToken(user)
    mainwin.setUser(newUser)
    print("new access token gotten")
    mainwin.newAccessTimer()

class MainWindow:
    def __init__(self, node: Node):
        super().__init__()
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

        self.trigger_action_client = create_action_client_wait_for_server(
            self.node, Trigger, 'robot_camera_test_node/test')
        self._action_client = ActionClient(self.node, Fibonacci, 'fibonacci')

        # setting up keyrock #
        # self.keyrockAPI = KeyrockAPI()

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
        self.ui.buttonSettings.clicked.connect(self.aisettings)

        # connecting radiobuttons
        self.ui.radioAI.toggled.connect(self.ai)
        self.ui.radioManual.toggled.connect(self.manual)
        self.ui.radioBoard.toggled.connect(self.leaderboard)
        self.ui.radioInteraction.toggled.connect(self.startInteraction)

        # logged in user info
        self.currentUser = LoggedInUser()
        self.accessTimer = None

        self.init_anyfeeder()

        self.show()

    def setUser(self, user):
        self.currentUser = user

    # def newAccessTimer(self):
    #     self.accessTimer = Timer(3500, endAccessTime, args=(self.keyrockAPI, self.currentUser, self))
    #     self.accessTimer.start()

    def login(self):
        username = self.ui.textUsername.text()
        password = self.ui.textPassword.text()

        # authenticate user using keyrock
        # result, self.currentUser = self.keyrockAPI.authenticateUser(username, password, self.currentUser)

        # if result:
        #     # success
        #     self.ui.labelRole.setText(self.currentUser.role)
        #     self.ui.labelUsername_2.setText(self.currentUser.username)

        # change to mainPage
        self.ui.stackedLogin.setCurrentWidget(self.ui.mainPage)
        self.ui.stackedPages.setCurrentWidget(self.ui.pageAI)
        self.ui.radioAI.toggle()

        # clear the login page
        self.ui.textPassword.clear()
        self.ui.textUsername.clear()
        self.ui.labelLoginError.hide()

        #     self.newAccessTimer()

        # else:
        #     # failure
        #     self.ui.labelLoginError.show()
        #     self.ui.textPassword.clear()
        #     self.ui.textUsername.clear()

        #     self.currentUser = LoggedInUser()

    def logout(self):
        self.ui.stackedLogin.setCurrentWidget(self.ui.loginPage)
        self.currentUser = LoggedInUser()
        self.accessTimer.cancel()

    def authorize(self, action, resource):
        return self.keyrockAPI.authorizeUser(self.currentUser, action, resource)

    def aisettings(self):
        if self.authorize("POST", "/ai"):
            print("you may change the settings")
        else:
            print("you may not change the settings")

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
            exec("self.ui.name{}.setText(p['name'])".format(i + 1))
            exec("self.ui.pickups{}.setText('{} pickups')".format(i + 1, p['score']))

    def startInteraction(self):
        self.ui.stackedLogin.setCurrentWidget(self.interactionui.getWidget())
        self.interactionui.startup()

    def endInteraction(self):
        self.ui.radioBoard.toggle()
        self.ui.stackedLogin.setCurrentWidget(self.ui.mainPage)
        self.leaderboard()

    def show(self):
        self.main_win.show()

    def close_application(self):
        # TODO: Close application correctly
        self.node.get_logger().info('application closing!')

    def trigger_cam(self):
        # TODO: set a bool to enable thread call only if not called before
        # set bool end of triggger camera callback
        thread = Thread(target=self.trigger_sensopart_camera)
        thread.start()
        thread.join()

    def trigger_sensopart_camera(self):
        future = self.trigger_action_client.send_goal_async(Trigger.Goal(), feedback_callback=self.feedback_callback)
        rclpy.spin_until_future_complete(self.node, future)
        trigger_handle = future.result()
        if not trigger_handle.accepted:
            self.node.get_logger().info('Goal rejected :(')
            return

        self.node.get_logger().info('Goal accepted :)')

        result_future = trigger_handle.get_result_async()
        rclpy.spin_until_future_complete(self.node, result_future)
        result: Trigger.Result() = result_future.result().result
        self.node.get_logger().info('Result: {0}'.format(result.message))
        # TODO: Test if success is set True when robot pick-up an object
        # Looks like that in code in robot_camera_test_node
        if result.success == True:
            self.node.get_logger().info("Picked-up an object!")
            self.node.get_logger().info(f"Received feedback: {result.message}")
            self.interactionui.pickupSuccess()
        else:
            self.node.get_logger().info("Nothing picked-up!")
            self.node.get_logger().info(f"Received feedback: {result.message}")

        # self.interactionui.set_enable_all_buttons(True)         

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.node.get_logger().info('Received feedback: {0}'.format(feedback.feedback))

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

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     main_win = MainWindow()
#     main_win.show()
#     sys.exit(app.exec_())
