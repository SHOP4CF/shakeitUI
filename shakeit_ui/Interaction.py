from PyQt5.QtWidgets import QWidget, QDialog
from shakeit_ui.InteractionUI import Ui_Interaction
from shakeit_ui.ExitDialog import ExitDialogWindow

import subprocess
from shakeit_ui import shakeitui_node

class InteractionWindow:

    def __init__(self, mainWindow):
        self.mainWindow = mainWindow

        # setting up UI #
        self.interaction = QWidget()
        self.ui = Ui_Interaction()
        self.ui.setupUi(self.interaction)

        # connecting buttons
        self.ui.buttonStart.clicked.connect(self.start)
        self.ui.buttonReady.clicked.connect(self.ready)
        self.ui.buttonEnd.clicked.connect(self.end)

        self.ui.buttonExit.clicked.connect(self.done)
        self.ui.buttonExit_2.clicked.connect(self.exit)
        self.ui.buttonExit_3.clicked.connect(self.exit)
        self.ui.buttonExit_4.clicked.connect(self.exit)

        # connecting buttons for anyfeeder
        self.ui.buttonforward.clicked.connect(self.trainforward)
        self.ui.buttonFlip.clicked.connect(self.trainflip)
        self.ui.buttonback.clicked.connect(self.trainbackward)

    def getWidget(self):
        return self.interaction

    def startup(self):
        self.ui.stackedpages.setCurrentWidget(self.ui.page1welcome)

    def start(self):
        self.ui.stackedpages.setCurrentWidget(self.ui.page2try)
        self.ui.textName.clear()

    def ready(self):
        self.ui.stackedpages.setCurrentWidget(self.ui.page3play)

    def end(self):
        self.ui.stackedpages.setCurrentWidget(self.ui.page4board)

    def exit(self):
        # before interaction completed
        result = ExitDialogWindow.launch(self.mainWindow.main_win)
        if result == 1:
            self.mainWindow.endInteraction()

    def done(self):
        # after interaction completed
        self.mainWindow.endInteraction()

    def trainforward(self):
        #ros2 service call /anyfeeder_node/init anyfeeder_interfaces/srv/StandardInput "{parameters: {repetitions: 0, speed: 0}}"
        fw_3_8 = subprocess.Popen(["ros2","service","call","/anyfeeder_node/feed_forward", "anyfeeder_interfaces/srv/StandardInput", """{parameters: {repetitions: 2, speed: 6}}"""], stdout=subprocess.PIPE)
        output = fw_3_8.communicate()[0]

    def trainflip(self):
        #ros2 service call /anyfeeder_node/init anyfeeder_interfaces/srv/StandardInput "{parameters: {repetitions: 0, speed: 0}}"
        fl_3_8 = subprocess.Popen(["ros2","service","call","/anyfeeder_node/flip", "anyfeeder_interfaces/srv/StandardInput", """{parameters: {repetitions: 2, speed: 6}}"""], stdout=subprocess.PIPE)
        output = fl_3_8.communicate()[0]

    def trainbackward(self):
        #ros2 service call /anyfeeder_node/init anyfeeder_interfaces/srv/StandardInput "{parameters: {repetitions: 0, speed: 0}}"
        fb_3_8 = subprocess.Popen(["ros2","service","call","/anyfeeder_node/feed_backward", "anyfeeder_interfaces/srv/StandardInput", """{parameters: {repetitions: 2, speed: 6}}"""], stdout=subprocess.PIPE)
        output = fb_3_8.communicate()[0]