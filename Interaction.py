import time
import json
from PyQt5.QtCore import pyqtSignal, QThread, QMutex, QWaitCondition
from PyQt5.QtWidgets import QWidget

from InteractionUI import Ui_Interaction
from ExitDialog import ExitDialogWindow
from TimesUpDialog import TimesUpDialog
from InfoDialog import InfoDialogWindow


class CountdownThread(QThread):
    finished = pyqtSignal()

    def __init__(self, startTime, mainwin):
        super().__init__()
        self.currentTime = startTime

        self.mutex = QMutex()
        self.condition = QWaitCondition()
        self.is_paused = False
        self.window = mainwin

    def run(self):
        while self.currentTime >= 0:
            self.window.ui.timer.display(self.currentTime)
            self.currentTime -= 1
            time.sleep(1)

            self.mutex.lock()
            while self.is_paused:
                self.condition.wait(self.mutex)
            self.mutex.unlock()

        self.finished.emit()

    def pause(self):
        if self.is_paused:
            self.resume()
        else:
            self.mutex.lock()
            self.is_paused = True
            self.mutex.unlock()

            print("paused")

    def resume(self):
        self.mutex.lock()
        self.is_paused = False
        self.condition.wakeAll()
        self.mutex.unlock()

        print("resumed")


class InteractionWindow:

    def __init__(self, mainWindow):
        self.mainWindow = mainWindow

        # setting up UI #
        self.interaction = QWidget()
        self.ui = Ui_Interaction()
        self.ui.setupUi(self.interaction)

        # set up countdown thread
        self.thread = None
        self.countdown = None

        # connecting buttons
        self.ui.textName.textChanged.connect(self.onTextChanged)
        self.ui.buttonStart.clicked.connect(self.tryShakeIt)
        self.ui.buttonStart.setEnabled(False)
        self.ui.buttonReady.clicked.connect(self.play)

        self.ui.pushButton_52.clicked.connect(self.pickupSuccess)

        self.ui.buttonExit_1.clicked.connect(self.exit)
        self.ui.buttonExit_2.clicked.connect(self.exit)
        self.ui.buttonExit_3.clicked.connect(self.done)

        # Initialize attributes #
        self.player = {
            "name": "",
            "score": 0
        }
        self.players = json.loads(open('leaderboard.json').read())
        self.mainWindow.updateLeaderboard(self.players)

        self.ai_score = "12"

    def getWidget(self):
        return self.interaction

    def makeCountDownThread(self):
        self.thread = QThread()
        self.countdown = CountdownThread(10, self)
        self.countdown.moveToThread(self.thread)

        self.thread.started.connect(self.countdown.start)
        self.countdown.finished.connect(self.timeOut)
        self.countdown.finished.connect(self.thread.quit)
        self.countdown.finished.connect(self.countdown.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.ui.pushButton_46.clicked.connect(self.countdown.pause)

        self.thread.start()

    def startup(self):
        self.ui.stackedpages.setCurrentWidget(self.ui.page1welcome)

    def onTextChanged(self):
        self.ui.buttonStart.setEnabled(bool(self.ui.textName.text()))

    def tryShakeIt(self):
        self.ui.stackedpages.setCurrentWidget(self.ui.page2try)
        self.player["name"] = self.ui.textName.text()

    def play(self):
        result = InfoDialogWindow.launch(self.mainWindow.main_win, self.ai_score)
        if result == 1:  # yes
            self.start()

    def start(self):
        self.ui.pickupDisplay.setText("{} pickups".format(self.player["score"]))
        self.ui.stackedpages.setCurrentWidget(self.ui.page3play)

        # Start countdown
        self.makeCountDownThread()

    def pickupSuccess(self):
        self.player["score"] += 1
        self.ui.pickupDisplay.setText("{} pickups".format(self.player["score"]))

    def timeOut(self):
        dialog = TimesUpDialog(self.player["score"], self.ai_score)
        result = dialog.exec()

        # wait for pop up to be closed
        if result == 0:

            # Adding player score til list of all players #

            if len(self.players) == 0:  # no other players
                self.players.append(self.player)
            else:
                if self.players[-1]["score"] >= self.player["score"]:  # smaller than the lowest number
                    self.players.append(self.player)
                elif self.player["score"] >= self.players[0]["score"]:  # larger than the highest number
                    self.players.insert(0, self.player)

                else:
                    i = 0
                    while i < len(self.players):
                        if self.players[i]["score"] > self.player["score"] >= self.players[i + 1]["score"]:
                            self.players.insert(i + 1, self.player)
                            break
                        i = i + 1

            json.dump(self.players, open('leaderboard.json', 'w'))

            # Updating leaderboard #
            for i, p in enumerate(self.players):
                if i > 9:
                    break
                exec("self.ui.name{}.setText(p['name'])".format(i + 1))
                exec("self.ui.pickups{}.setText('{} pickups')".format(i + 1, p['score']))

            self.ui.playernum.setText(str(self.players.index(self.player) + 1))
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
