import time
import json
from PyQt5.QtCore import pyqtSignal, QThread, QMutex, QWaitCondition, QTimer
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

    def __init__(self, main_window):
        self.main_window = main_window

        # setting up UI #
        self.interaction = QWidget()
        self.ui = Ui_Interaction()
        self.ui.setupUi(self.interaction)

        # set up countdown thread
        self.thread = None
        self.countdown = None
        self.timer = None

        # connecting buttons
        self.ui.textName.textChanged.connect(self.on_text_changed)
        self.ui.buttonStart.clicked.connect(self.try_shakeit)
        self.ui.buttonStart.setEnabled(False)
        self.ui.buttonReady.clicked.connect(self.play)

        self.ui.pushButton_52.clicked.connect(self.pickup_success)

        self.ui.buttonExit_1.clicked.connect(self.exit)
        self.ui.buttonExit_2.clicked.connect(self.exit)
        self.ui.buttonExit_3.clicked.connect(self.done)

        # Initialize attributes #
        self.ai_score = "12"
        self.player = {
            "name": "",
            "score": 0
        }
        self.players = json.loads(open('leaderboard.json').read())
        self.main_window.update_leaderboard(self.players)

    def get_widget(self):
        return self.interaction

    def make_countdown_thread(self):
        self.thread = QThread()
        self.countdown = CountdownThread(60, self)
        self.countdown.moveToThread(self.thread)

        self.thread.started.connect(self.countdown.start)
        self.countdown.finished.connect(self.time_out)
        self.countdown.finished.connect(self.thread.quit)
        self.countdown.finished.connect(self.countdown.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.ui.pushButton_46.clicked.connect(self.countdown.pause)

        self.thread.start()

    def startup(self):
        self.ui.stackedpages.setCurrentWidget(self.ui.page1welcome)

    def on_text_changed(self):
        self.ui.buttonStart.setEnabled(bool(self.ui.textName.text()))  # enable button if there is text

    def try_shakeit(self):
        self.ui.stackedpages.setCurrentWidget(self.ui.page2try)
        self.player["name"] = self.ui.textName.text()

    def play(self):
        result = InfoDialogWindow.launch(self.main_window.main_win, self.ai_score)
        if result == 1:  # yes
            self.start()

    def start(self):
        self.ui.pickupDisplay.setText("0 pickups")
        self.ui.stackedpages.setCurrentWidget(self.ui.page3play)

        # Start countdown
        self.make_countdown_thread()

    def pickup_success(self):
        self.player["score"] += 1
        self.ui.pickupDisplay.setText("{} pickups".format(self.player["score"]))

    def time_out(self):
        dialog = TimesUpDialog(self.player["score"], self.ai_score)
        result = dialog.exec()

        # wait for pop up to be closed
        if result == 0:

            # Adding player score til list of all players #
            player_score = self.player["score"]
            if not self.players:
                # no other players
                self.players.append(self.player)
            elif player_score <= self.players[-1]["score"]:
                # smaller than the lowest number
                self.players.append(self.player)
            elif player_score >= self.players[0]["score"]:
                # larger than the highest number
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
            name_labels = [getattr(self.ui, f"name{i}") for i in range(1, 11)]
            pickup_labels = [getattr(self.ui, f"pickups{i}") for i in range(1, 11)]

            for i, p in enumerate(self.players[:10]):
                name_labels[i].setText(p['name'])
                pickup_labels[i].setText(f"{p['score']} pickups")

            self.ui.playernum.setText(str(self.players.index(self.player) + 1))
            self.ui.playername.setText(self.player["name"])
            self.ui.playerpickups.setText("{} pickups".format(self.player["score"]))

            self.main_window.update_leaderboard(self.players)

            self.ui.stackedpages.setCurrentWidget(self.ui.page4board)

            # switch back to welcome screen after inaction
            self.timer = QTimer(self.main_window.main_win)
            self.timer.setInterval(25000)  # waits 25 seconds
            self.timer.timeout.connect(self.restart)
            self.timer.start()

    def restart(self):
        self.timer.stop()
        self.clear_player_info()
        self.startup()  # Back to welcome screen

    def exit(self):
        # exit before interaction completed
        result = ExitDialogWindow.launch(self.main_window.main_win)
        if result == 1:  # yes
            self.clear_player_info()
            self.main_window.end_interaction()  # Back to main screen

    def done(self):
        # exit after interaction completed
        self.timer.stop()
        self.clear_player_info()
        self.main_window.end_interaction()  # Back to main screen

    def clear_player_info(self):
        self.player = {
            "name": "",
            "score": 0
        }
        self.ui.textName.clear()
