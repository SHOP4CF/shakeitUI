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
