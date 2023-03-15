from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer
import json

from InteractionUI import Ui_Interaction
from ExitDialog import ExitDialogWindow
from TimesUpDialog import TimesUpDialogWindow


class InteractionWindow:

    def __init__(self, mainWindow):
        self.mainWindow = mainWindow

        # setting up UI #
        self.interaction = QWidget()
        self.ui = Ui_Interaction()
        self.ui.setupUi(self.interaction)

        # connecting buttons
        self.ui.textName.textChanged.connect(self.onTextChanged)
        self.ui.buttonStart.clicked.connect(self.tryShakeIt)
        self.ui.buttonStart.setEnabled(False)
        self.ui.buttonReady.clicked.connect(self.play)
        self.ui.pushButton_52.clicked.connect(self.pickupSuccess)

        self.ui.buttonExit_1.clicked.connect(self.exit)
        self.ui.buttonExit_2.clicked.connect(self.exit)
        self.ui.buttonExit_3.clicked.connect(self.done)

        # connecting training buttons for anyfeeder
        self.ui.buttonforward.clicked.connect(self.trainforward)
        self.ui.buttonFlip.clicked.connect(self.trainflip)
        self.ui.buttonback.clicked.connect(self.trainbackward)

        # connecting buttons for anyfeeder
        # btn shake forward
        self.ui.pushButton_52.clicked.connect(self.fw_s2_r1)
        self.ui.pushButton_45.clicked.connect(self.fw_s4_r1)
        self.ui.pushButton_48.clicked.connect(self.fw_s6_r1)
        self.ui.pushButton_43.clicked.connect(self.fw_s8_r1)
        self.ui.pushButton_47.clicked.connect(self.fw_s10_r1)
        self.ui.pushButton_46.clicked.connect(self.fw_s2_r3)
        self.ui.pushButton_44.clicked.connect(self.fw_s4_r3)
        self.ui.pushButton_50.clicked.connect(self.fw_s6_r3)
        self.ui.pushButton_51.clicked.connect(self.fw_s8_r3)
        self.ui.pushButton_49.clicked.connect(self.fw_s10_r3)

        # btn shake flip
        self.ui.buttonEnd.clicked.connect(self.flip_s2_r1)
        self.ui.pushButton_35.clicked.connect(self.flip_s4_r1)
        self.ui.pushButton_38.clicked.connect(self.flip_s6_r1)
        self.ui.pushButton_33.clicked.connect(self.flip_s8_r1)
        self.ui.pushButton_37.clicked.connect(self.flip_s10_r1)
        self.ui.pushButton_36.clicked.connect(self.flip_s2_r3)
        self.ui.pushButton_34.clicked.connect(self.flip_s4_r3)
        self.ui.pushButton_40.clicked.connect(self.flip_s6_r3)
        self.ui.pushButton_41.clicked.connect(self.flip_s8_r3)
        self.ui.pushButton_39.clicked.connect(self.flip_s10_r3)

        # btn shake backward
        self.ui.pushButton_32.clicked.connect(self.bw_s2_r1)
        self.ui.pushButton_25.clicked.connect(self.bw_s4_r1)
        self.ui.pushButton_28.clicked.connect(self.bw_s6_r1)
        self.ui.pushButton_23.clicked.connect(self.bw_s8_r1)
        self.ui.pushButton_27.clicked.connect(self.bw_s10_r1)
        self.ui.pushButton_26.clicked.connect(self.bw_s2_r3)
        self.ui.pushButton_24.clicked.connect(self.bw_s4_r3)
        self.ui.pushButton_30.clicked.connect(self.bw_s6_r3)
        self.ui.pushButton_31.clicked.connect(self.bw_s8_r3)
        self.ui.pushButton_29.clicked.connect(self.bw_s10_r3)

        # setting up timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.showTime)
        self.timerTime = 60
        self.currentTime = self.timerTime

        # Initialize attributes #
        self.player = {
            "name": "",
            "score": 0
        }
        self.players = json.loads(open('leaderboard.json').read())
        self.mainWindow.updateLeaderboard(self.players)

    def getWidget(self):
        return self.interaction

    def startup(self):
        self.ui.stackedpages.setCurrentWidget(self.ui.page1welcome)

    def onTextChanged(self):
        self.ui.buttonStart.setEnabled(bool(self.ui.textName.text()))

    def tryShakeIt(self):
        self.ui.stackedpages.setCurrentWidget(self.ui.page2try)
        self.player["name"] = self.ui.textName.text()

    def play(self):
        # setting timer and score to initial
        self.currentTime = self.timerTime
        self.ui.timer.display(self.currentTime)
        self.ui.pickupDisplay.setText("{} pickups".format(self.player["score"]))

        self.ui.stackedpages.setCurrentWidget(self.ui.page3play)
        self.timer.start(1000)

    def pickupSuccess(self):
        self.player["score"] += 1
        self.ui.pickupDisplay.setText("{} pickups".format(self.player["score"]))

    def showTime(self):
        self.currentTime = self.currentTime - 1
        self.ui.timer.display(self.currentTime)

        if self.currentTime == 0:
            self.timer.stop()

            result = TimesUpDialogWindow.launch(self.mainWindow.main_win, self.player["score"], "12")
            if result == 0:
                self.timeOut()

    def timeOut(self):
        # Adding player score til list of all players #
        score = self.player["score"]

        if len(self.players) == 0:  # no other players
            self.players.append(self.player)
        else:
            if self.players[-1]["score"] >= score:  # smaller than the lowest number
                self.players.append(self.player)
            elif score >= self.players[0]["score"]:  # larger than the highest number
                self.players.insert(0, self.player)

            else:
                i = 0
                while i < len(self.players):
                    if self.players[i]["score"] > score >= self.players[i+1]["score"]:
                        self.players.insert(i+1, self.player)
                        break
                    i = i + 1

        json.dump(self.players, open('leaderboard.json', 'w'))

        # Updating leaderboard #
        for i, p in enumerate(self.players):
            if i > 9:
                break
            exec("self.ui.name{}.setText(p['name'])".format(i+1))
            exec("self.ui.pickups{}.setText('{} pickups')".format(i+1, p['score']))

        self.ui.playernum.setText(str(self.players.index(self.player)+1))
        self.ui.playername.setText(self.player["name"])
        self.ui.playerpickups.setText("{} pickups".format(self.player["score"]))

        self.mainWindow.updateLeaderboard(self.players)

        self.ui.stackedpages.setCurrentWidget(self.ui.page4board)

    def exit(self):
        # before interaction completed
        result = ExitDialogWindow.launch(self.mainWindow.main_win)
        if result == 1:
            self.mainWindow.endInteraction()
            self.ui.textName.clear()

            # deleting info on player
            self.player = {
                "name": "",
                "score": 0
            }

    def done(self):
        # after interaction completed
        self.mainWindow.endInteraction()
        self.ui.textName.clear()

        # deleting info on player
        self.player = {
            "name": "",
            "score": 0
        }

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

    #
    # FORWARD CMDs
    #

    def fw_s2_r1(self):
        fw_2_1 = subprocess.Popen(["ros2","service","call","/anyfeeder_node/feed_forward", "anyfeeder_interfaces/srv/StandardInput", """{parameters: {repetitions: 1, speed: 2}}"""], stdout=subprocess.PIPE)
        output = fw_2_1.communicate()[0]
        self.trigger_cam()
    
    def fw_s4_r1(self):
        fw_4_1 = subprocess.Popen(["ros2","service","call","/anyfeeder_node/feed_forward", "anyfeeder_interfaces/srv/StandardInput", """{parameters: {repetitions: 1, speed: 4}}"""], stdout=subprocess.PIPE)
        output = fw_4_1.communicate()[0]
        self.trigger_cam()

    def fw_s6_r1(self):
        fw_6_1 = subprocess.Popen(["ros2","service","call","/anyfeeder_node/feed_forward", "anyfeeder_interfaces/srv/StandardInput", """{parameters: {repetitions: 1, speed: 6}}"""], stdout=subprocess.PIPE)
        output = fw_6_1.communicate()[0]
        self.trigger_cam()

    def fw_s8_r1(self):
        fw_8_1 = subprocess.Popen(["ros2","service","call","/anyfeeder_node/feed_forward", "anyfeeder_interfaces/srv/StandardInput", """{parameters: {repetitions: 1, speed: 8}}"""], stdout=subprocess.PIPE)
        output = fw_8_1.communicate()[0]
        self.trigger_cam()

    def fw_s10_r1(self):
        fw_10_1 = subprocess.Popen(["ros2","service","call","/anyfeeder_node/feed_forward", "anyfeeder_interfaces/srv/StandardInput", """{parameters: {repetitions: 1, speed: 10}}"""], stdout=subprocess.PIPE)
        output = fw_10_1.communicate()[0]
        self.trigger_cam()

    def fw_s2_r3(self):
        fw_2_1 = subprocess.Popen(["ros2","service","call","/anyfeeder_node/feed_forward", "anyfeeder_interfaces/srv/StandardInput", """{parameters: {repetitions: 3, speed: 2}}"""], stdout=subprocess.PIPE)
        output = fw_2_1.communicate()[0]
        self.trigger_cam()
    
    def fw_s4_r3(self):
        fw_4_1 = subprocess.Popen(["ros2","service","call","/anyfeeder_node/feed_forward", "anyfeeder_interfaces/srv/StandardInput", """{parameters: {repetitions: 3, speed: 4}}"""], stdout=subprocess.PIPE)
        output = fw_4_1.communicate()[0]
        self.trigger_cam()

    def fw_s6_r3(self):
        fw_6_1 = subprocess.Popen(["ros2","service","call","/anyfeeder_node/feed_forward", "anyfeeder_interfaces/srv/StandardInput", """{parameters: {repetitions: 3, speed: 6}}"""], stdout=subprocess.PIPE)
        output = fw_6_1.communicate()[0]
        self.trigger_cam()

    def fw_s8_r3(self):
        fw_8_1 = subprocess.Popen(["ros2","service","call","/anyfeeder_node/feed_forward", "anyfeeder_interfaces/srv/StandardInput", """{parameters: {repetitions: 3, speed: 8}}"""], stdout=subprocess.PIPE)
        output = fw_8_1.communicate()[0]
        self.trigger_cam()

    def fw_s10_r3(self):
        fw_10_1 = subprocess.Popen(["ros2","service","call","/anyfeeder_node/feed_forward", "anyfeeder_interfaces/srv/StandardInput", """{parameters: {repetitions: 3, speed: 10}}"""], stdout=subprocess.PIPE)
        output = fw_10_1.communicate()[0]
        self.trigger_cam()

    #
    # FLIP CMDs
    #     

    def flip_s2_r1(self):
        flip_2_1 = subprocess.Popen(["ros2","service","call","/anyfeeder_node/flip", "anyfeeder_interfaces/srv/StandardInput", """{parameters: {repetitions: 1, speed: 2}}"""], stdout=subprocess.PIPE)
        output = flip_2_1.communicate()[0]
        self.trigger_cam()
    
    def flip_s4_r1(self):
        flip_4_1 = subprocess.Popen(["ros2","service","call","/anyfeeder_node/flip", "anyfeeder_interfaces/srv/StandardInput", """{parameters: {repetitions: 1, speed: 4}}"""], stdout=subprocess.PIPE)
        output = flip_4_1.communicate()[0]
        self.trigger_cam()

    def flip_s6_r1(self):
        flip_6_1 = subprocess.Popen(["ros2","service","call","/anyfeeder_node/flip", "anyfeeder_interfaces/srv/StandardInput", """{parameters: {repetitions: 1, speed: 6}}"""], stdout=subprocess.PIPE)
        output = flip_6_1.communicate()[0]
        self.trigger_cam()

    def flip_s8_r1(self):
        flip_8_1 = subprocess.Popen(["ros2","service","call","/anyfeeder_node/flip", "anyfeeder_interfaces/srv/StandardInput", """{parameters: {repetitions: 1, speed: 8}}"""], stdout=subprocess.PIPE)
        output = flip_8_1.communicate()[0]
        self.trigger_cam()

    def flip_s10_r1(self):
        flip_10_1 = subprocess.Popen(["ros2","service","call","/anyfeeder_node/flip", "anyfeeder_interfaces/srv/StandardInput", """{parameters: {repetitions: 1, speed: 10}}"""], stdout=subprocess.PIPE)
        output = flip_10_1.communicate()[0]
        self.trigger_cam()

    def flip_s2_r3(self):
        flip_2_1 = subprocess.Popen(["ros2","service","call","/anyfeeder_node/flip", "anyfeeder_interfaces/srv/StandardInput", """{parameters: {repetitions: 3, speed: 2}}"""], stdout=subprocess.PIPE)
        output = flip_2_1.communicate()[0]
        self.trigger_cam()
    
    def flip_s4_r3(self):
        flip_4_1 = subprocess.Popen(["ros2","service","call","/anyfeeder_node/flip", "anyfeeder_interfaces/srv/StandardInput", """{parameters: {repetitions: 3, speed: 4}}"""], stdout=subprocess.PIPE)
        output = flip_4_1.communicate()[0]
        self.trigger_cam()

    def flip_s6_r3(self):
        flip_6_1 = subprocess.Popen(["ros2","service","call","/anyfeeder_node/flip", "anyfeeder_interfaces/srv/StandardInput", """{parameters: {repetitions: 3, speed: 6}}"""], stdout=subprocess.PIPE)
        output = flip_6_1.communicate()[0]
        self.trigger_cam()

    def flip_s8_r3(self):
        flip_8_1 = subprocess.Popen(["ros2","service","call","/anyfeeder_node/flip", "anyfeeder_interfaces/srv/StandardInput", """{parameters: {repetitions: 3, speed: 8}}"""], stdout=subprocess.PIPE)
        output = flip_8_1.communicate()[0]
        self.trigger_cam()

    def flip_s10_r3(self):
        flip_10_1 = subprocess.Popen(["ros2","service","call","/anyfeeder_node/flip", "anyfeeder_interfaces/srv/StandardInput", """{parameters: {repetitions: 3, speed: 10}}"""], stdout=subprocess.PIPE)
        output = flip_10_1.communicate()[0]
        self.trigger_cam()

    #
    # BACWARDS CMDs
    #     

    def bw_s2_r1(self):
        bw_2_1 = subprocess.Popen(["ros2","service","call","/anyfeeder_node/feed_backward", "anyfeeder_interfaces/srv/StandardInput", """{parameters: {repetitions: 1, speed: 2}}"""], stdout=subprocess.PIPE)
        output = bw_2_1.communicate()[0]
        self.trigger_cam()
    
    def bw_s4_r1(self):
        bw_4_1 = subprocess.Popen(["ros2","service","call","/anyfeeder_node/feed_backward", "anyfeeder_interfaces/srv/StandardInput", """{parameters: {repetitions: 1, speed: 4}}"""], stdout=subprocess.PIPE)
        output = bw_4_1.communicate()[0]
        self.trigger_cam()

    def bw_s6_r1(self):
        bw_6_1 = subprocess.Popen(["ros2","service","call","/anyfeeder_node/feed_backward", "anyfeeder_interfaces/srv/StandardInput", """{parameters: {repetitions: 1, speed: 6}}"""], stdout=subprocess.PIPE)
        output = bw_6_1.communicate()[0]
        self.trigger_cam()

    def bw_s8_r1(self):
        bw_8_1 = subprocess.Popen(["ros2","service","call","/anyfeeder_node/feed_backward", "anyfeeder_interfaces/srv/StandardInput", """{parameters: {repetitions: 1, speed: 8}}"""], stdout=subprocess.PIPE)
        output = bw_8_1.communicate()[0]
        self.trigger_cam()

    def bw_s10_r1(self):
        bw_10_1 = subprocess.Popen(["ros2","service","call","/anyfeeder_node/feed_backward", "anyfeeder_interfaces/srv/StandardInput", """{parameters: {repetitions: 1, speed: 10}}"""], stdout=subprocess.PIPE)
        output = bw_10_1.communicate()[0]
        self.trigger_cam()

    def bw_s2_r3(self):
        bw_2_1 = subprocess.Popen(["ros2","service","call","/anyfeeder_node/feed_backward", "anyfeeder_interfaces/srv/StandardInput", """{parameters: {repetitions: 3, speed: 2}}"""], stdout=subprocess.PIPE)
        output = bw_2_1.communicate()[0]
        self.trigger_cam()
    
    def bw_s4_r3(self):
        bw_4_1 = subprocess.Popen(["ros2","service","call","/anyfeeder_node/feed_backward", "anyfeeder_interfaces/srv/StandardInput", """{parameters: {repetitions: 3, speed: 4}}"""], stdout=subprocess.PIPE)
        output = bw_4_1.communicate()[0]
        self.trigger_cam()

    def bw_s6_r3(self):
        bw_6_1 = subprocess.Popen(["ros2","service","call","/anyfeeder_node/feed_backward", "anyfeeder_interfaces/srv/StandardInput", """{parameters: {repetitions: 3, speed: 6}}"""], stdout=subprocess.PIPE)
        output = bw_6_1.communicate()[0]
        self.trigger_cam()

    def bw_s8_r3(self):
        bw_8_1 = subprocess.Popen(["ros2","service","call","/anyfeeder_node/feed_backward", "anyfeeder_interfaces/srv/StandardInput", """{parameters: {repetitions: 3, speed: 8}}"""], stdout=subprocess.PIPE)
        output = bw_8_1.communicate()[0]
        self.trigger_cam()

    def bw_s10_r3(self):
        bw_10_1 = subprocess.Popen(["ros2","service","call","/anyfeeder_node/feed_backward", "anyfeeder_interfaces/srv/StandardInput", """{parameters: {repetitions: 3, speed: 10}}"""], stdout=subprocess.PIPE)
        output = bw_10_1.communicate()[0]
        self.trigger_cam()

    def trigger_cam(self):
        print("Trigger cam")
        # ros2 action send_goal /robot_camera_test_node/test shakeit_interfaces/action/Trigger {}
        trigger = subprocess.Popen(["ros2","action","send_goal","/robot_camera_test_node/test", "shakeit_interfaces/action/Trigger", """{}"""], stdout=subprocess.PIPE)
        output = trigger.communicate()[0]
