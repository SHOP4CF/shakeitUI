from PyQt5.QtWidgets import QWidget
from InteractionUI import Ui_Interaction


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
        self.mainWindow.endInteraction()

    def done(self):
        # after interaction completed
        self.mainWindow.endInteraction()
