from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer
import json

from shakeit_ui.InteractionUI import Ui_Interaction
from shakeit_ui.ExitDialog import ExitDialogWindow
from shakeit_ui.TimesUpDialog import TimesUpDialogWindow

# Import anyfeeder
from rclpy.node import Node


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
        self.ui.pushButton_42.clicked.connect(self.flip_s2_r1)
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
        self.ui.pushButton_76.clicked.connect(self.bw_s2_r1)
        self.ui.pushButton_78.clicked.connect(self.bw_s4_r1)
        self.ui.pushButton_74.clicked.connect(self.bw_s6_r1)
        self.ui.pushButton_81.clicked.connect(self.bw_s8_r1)
        self.ui.pushButton_82.clicked.connect(self.bw_s10_r1)
        self.ui.pushButton_73.clicked.connect(self.bw_s2_r3)
        self.ui.pushButton_79.clicked.connect(self.bw_s4_r3)
        self.ui.pushButton_77.clicked.connect(self.bw_s6_r3)
        self.ui.pushButton_80.clicked.connect(self.bw_s8_r3)
        self.ui.pushButton_75.clicked.connect(self.bw_s10_r3)

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
        self.players = json.loads(open('/home/dti/wspace/shakeit/ros_pkg_ws/src/shakeit_ui/resource/leaderboard.json').read())
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

        json.dump(self.players, open('/home/dti/wspace/shakeit/ros_pkg_ws/src/shakeit_ui/resource/leaderboard.json', 'w'))

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

    #
    # Training + dispense
    #

    def dispense(self):
        self.mainWindow.add_objects()

    def trainforward(self):
        self.mainWindow.forward_objects(2, 6)

    def trainflip(self):
        self.mainWindow.flip_objects(2, 6)

    def trainbackward(self):
        self.mainWindow.backward_objects(2, 6)

    #
    # FORWARD CMDs
    #

    def fw_s2_r1(self):
        self.dispense()
        #self.mainWindow.forward_objects(1, 2)
        self.mainWindow.trigger_sensopart_camera()
    
    def fw_s4_r1(self):
        self.mainWindow.forward_objects(1, 4)
        self.mainWindow.trigger_sensopart_camera()

    def fw_s6_r1(self):
        self.mainWindow.forward_objects(1, 6)
        self.mainWindow.trigger_sensopart_camera()

    def fw_s8_r1(self):
        self.mainWindow.forward_objects(1, 8)
        self.mainWindow.trigger_sensopart_camera()

    def fw_s10_r1(self):
        self.mainWindow.forward_objects(1, 10)
        self.mainWindow.trigger_sensopart_camera()

    def fw_s2_r3(self):
        self.mainWindow.forward_objects(3, 2)
        self.mainWindow.trigger_sensopart_camera()
    
    def fw_s4_r3(self):
        self.mainWindow.forward_objects(3, 4)
        self.mainWindow.trigger_sensopart_camera()

    def fw_s6_r3(self):
        self.mainWindow.forward_objects(3, 6)
        self.mainWindow.trigger_sensopart_camera()

    def fw_s8_r3(self):
        self.mainWindow.forward_objects(3, 8)
        self.mainWindow.trigger_sensopart_camera()

    def fw_s10_r3(self):
        self.mainWindow.forward_objects(3, 10)
        self.mainWindow.trigger_sensopart_camera()

    #
    # FLIP CMDs
    #     

    def flip_s2_r1(self):
        self.mainWindow.flip_objects(1, 2)
        self.mainWindow.trigger_sensopart_camera()
    
    def flip_s4_r1(self):
        self.mainWindow.flip_objects(1, 4)
        self.mainWindow.trigger_sensopart_camera()

    def flip_s6_r1(self):
        self.mainWindow.flip_objects(1, 6)
        self.mainWindow.trigger_sensopart_camera()

    def flip_s8_r1(self):
        self.mainWindow.flip_objects(1, 8)
        self.mainWindow.trigger_sensopart_camera()

    def flip_s10_r1(self):
        self.mainWindow.flip_objects(1, 10)
        self.mainWindow.trigger_sensopart_camera()

    def flip_s2_r3(self):
        self.mainWindow.flip_objects(3, 2)
        self.mainWindow.trigger_sensopart_camera()
    
    def flip_s4_r3(self):
        self.mainWindow.flip_objects(3, 4)
        self.mainWindow.trigger_sensopart_camera()

    def flip_s6_r3(self):
        self.mainWindow.flip_objects(3, 6)
        self.mainWindow.trigger_sensopart_camera()

    def flip_s8_r3(self):
        self.mainWindow.flip_objects(3, 8)
        self.mainWindow.trigger_sensopart_camera()

    def flip_s10_r3(self):
        self.mainWindow.flip_objects(3, 10)
        self.mainWindow.trigger_sensopart_camera()

    #
    # BACWARDS CMDs
    #     

    def bw_s2_r1(self):
        self.mainWindow.backward_objects(1, 2)
        self.mainWindow.trigger_sensopart_camera()
    
    def bw_s4_r1(self):
        self.mainWindow.backward_objects(1, 4)
        self.mainWindow.trigger_sensopart_camera()

    def bw_s6_r1(self):
        self.mainWindow.backward_objects(1, 6)
        self.mainWindow.trigger_sensopart_camera()

    def bw_s8_r1(self):
        self.mainWindow.backward_objects(1, 8)
        self.mainWindow.trigger_sensopart_camera()

    def bw_s10_r1(self):
        self.mainWindow.backward_objects(1, 10)
        self.mainWindow.trigger_sensopart_camera()

    def bw_s2_r3(self):
        self.mainWindow.backward_objects(3, 2)
        self.mainWindow.trigger_sensopart_camera()
    
    def bw_s4_r3(self):
        self.mainWindow.backward_objects(3, 4)
        self.mainWindow.trigger_sensopart_camera()

    def bw_s6_r3(self):
        self.mainWindow.backward_objects(3, 6)
        self.mainWindow.trigger_sensopart_camera()

    def bw_s8_r3(self):
        self.mainWindow.backward_objects(3, 8)
        self.mainWindow.trigger_sensopart_camera()

    def bw_s10_r3(self):
        self.mainWindow.backward_objects(3, 10)
        self.mainWindow.trigger_sensopart_camera()
