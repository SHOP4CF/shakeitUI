import sys
from threading import Timer

from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit
from MainUI import Ui_MainWindow
from Interaction import InteractionWindow
from KeyrockAPI import KeyrockAPI
from User import LoggedInUser


def endAccessTime(api, user, mainwin):
    newUser = api.refreshToken(user)
    mainwin.setUser(newUser)
    print("new access token gotten")
    mainwin.newAccessTimer()


class MainWindow:
    def __init__(self):
        # setting up keyrock
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

        # logged in user info
        self.currentUser = LoggedInUser()
        self.accessTimer = None

    def setUser(self, user):
        self.currentUser = user

    def newAccessTimer(self):
        self.accessTimer = Timer(3500, endAccessTime, args=(self.keyrockAPI, self.currentUser, self))
        self.accessTimer.start()

    def login(self):
        username = self.ui.textUsername.text()
        password = self.ui.textPassword.text()

        # authenticate user using keyrock
        result, self.currentUser = self.keyrockAPI.authenticateUser(username, password, self.currentUser)

        if result:
            # success
            self.ui.labelRole.setText(self.currentUser.role)
            self.ui.labelUsername_2.setText(self.currentUser.username)

            # change to mainPage
            self.ui.stackedLogin.setCurrentWidget(self.ui.mainPage)
            self.ui.stackedPages.setCurrentWidget(self.ui.pageAI)
            self.ui.radioAI.toggle()

            # clear the login page
            self.ui.textPassword.clear()
            self.ui.textUsername.clear()
            self.ui.labelLoginError.hide()

            self.newAccessTimer()

        else:
            # failure
            self.ui.labelLoginError.show()
            self.ui.textPassword.clear()
            self.ui.textUsername.clear()

            self.currentUser = LoggedInUser()

    def logout(self):
        self.ui.stackedLogin.setCurrentWidget(self.ui.loginPage)
        self.currentUser = LoggedInUser()
        self.accessTimer.cancel()

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())
