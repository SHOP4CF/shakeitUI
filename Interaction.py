from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer

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
        self.ui.buttonStart.clicked.connect(self.tryShakeIt)
        self.ui.buttonReady.clicked.connect(self.play)

        self.ui.buttonExit_1.clicked.connect(self.exit)
        self.ui.buttonExit_2.clicked.connect(self.exit)
        self.ui.buttonExit_3.clicked.connect(self.exit)
        self.ui.buttonExit_4.clicked.connect(self.done)

        # setting up timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.showTime)
        self.currentTime = 60
        self.ui.timer.display(self.currentTime)

        # Initialize attributes #
        self.playerName = ""
        self.playerScore = 0

    def getWidget(self):
        return self.interaction

    def startup(self):
        self.ui.stackedpages.setCurrentWidget(self.ui.page1welcome)

    def tryShakeIt(self):
        self.ui.stackedpages.setCurrentWidget(self.ui.page2try)
        self.ui.textName.clear()

    def play(self):
        self.ui.stackedpages.setCurrentWidget(self.ui.page3play)
        self.timer.start(1000)

    def showTime(self):
        self.currentTime = self.currentTime - 1
        self.ui.timer.display(self.currentTime)

        if self.currentTime == 0:
            self.timer.stop()

            result = TimesUpDialogWindow.launch(self.mainWindow.main_win, "1", "12")
            if result == 0:
                self.timeOut()

    def timeOut(self):
        self.ui.stackedpages.setCurrentWidget(self.ui.page4board)
        self.currentTime = 60
        self.ui.timer.display(self.currentTime)

    def exit(self):
        # before interaction completed
        result = ExitDialogWindow.launch(self.mainWindow.main_win)
        if result == 1:
            self.mainWindow.endInteraction()

    def done(self):
        # after interaction completed
        self.mainWindow.endInteraction()
