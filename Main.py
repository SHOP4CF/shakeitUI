import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit
from MainUI import Ui_MainWindow
from Interaction import InteractionWindow
from KeyrockAPI import KeyrockAPI


class MainWindow:
    def __init__(self):
        # setting up keyrock #
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


    def login(self):
        username = self.ui.textUsername.text()
        password = self.ui.textPassword.text()

        # authenticate user using keyrock
        result, accessToken = self.keyrockAPI.authenticateUser(username, password)

        if result:
            # success
            userInfo = self.keyrockAPI.getUserInfo(accessToken)

            try:
                self.ui.labelRole.setText(userInfo['roles'][0]['name'])
            except:
                self.ui.labelRole.setText("")

            self.ui.labelUsername_2.setText(userInfo['username'])

            # change to mainPage
            self.ui.stackedLogin.setCurrentWidget(self.ui.mainPage)
            self.ui.stackedPages.setCurrentWidget(self.ui.pageAI)
            self.ui.radioAI.toggle()

            # clear the login page
            self.ui.textPassword.clear()
            self.ui.textUsername.clear()
            self.ui.labelLoginError.hide()

        else:
            # failure
            self.ui.labelLoginError.show()
            self.ui.textPassword.clear()
            self.ui.textUsername.clear()

    def logout(self):
        self.ui.stackedLogin.setCurrentWidget(self.ui.loginPage)

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
