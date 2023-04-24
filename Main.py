import sys
from threading import Timer

from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit
from MainUI import Ui_MainWindow
from Interaction import InteractionWindow
from KeyrockAPI import KeyrockAPI
from User import LoggedInUser


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
        self.ui.stackedLogin.addWidget(self.interactionui.get_widget())

        # connecting buttons
        self.ui.buttonLogin.clicked.connect(self.login)
        self.ui.buttonLogout.clicked.connect(self.logout)
        self.ui.buttonSettings.clicked.connect(self.ai_settings)

        # connecting radiobuttons
        self.ui.radioAI.toggled.connect(self.ai)
        self.ui.radioManual.toggled.connect(self.manual)
        self.ui.radioBoard.toggled.connect(self.leaderboard)
        self.ui.radioInteraction.toggled.connect(self.start_interaction)

        # logged in user info
        self.current_user = LoggedInUser()

    def new_access_timer(self):
        accessTimer = Timer(3500, self.refresh_access_token)
        accessTimer.start()

    def refresh_access_token(self):
        self.current_user = self.keyrockAPI.refresh_token(self.current_user)
        print("new access token gotten")
        self.new_access_timer()

    def login(self):
        username = self.ui.textUsername.text()
        password = self.ui.textPassword.text()

        # authenticate user using keyrock
        result, self.current_user = self.keyrockAPI.authenticate_user(username, password, self.current_user)

        if result:  # success
            self.ui.labelRole.setText(self.current_user.role)
            self.ui.labelUsername_2.setText(self.current_user.username)

            # change to mainPage
            self.ui.stackedLogin.setCurrentWidget(self.ui.mainPage)
            self.ui.stackedPages.setCurrentWidget(self.ui.pageAI)
            self.ui.radioAI.toggle()

            # clear the login page
            self.ui.textPassword.clear()
            self.ui.textUsername.clear()
            self.ui.labelLoginError.hide()

            self.new_access_timer()

        else:  # failure
            # clear the login page
            self.ui.labelLoginError.show()
            self.ui.textPassword.clear()
            self.ui.textUsername.clear()
            self.current_user = LoggedInUser()

    def logout(self):
        self.ui.stackedLogin.setCurrentWidget(self.ui.loginPage)
        self.current_user = LoggedInUser()
        self.accessTimer.cancel()

    def authorize(self, action, resource):
        return self.keyrockAPI.authorize_user(self.current_user, action, resource)

    def ai_settings(self):
        if self.authorize("POST", "/ai"):
            print("you may change the settings")
        else:
            print("you may not change the settings")

    def ai(self):
        self.ui.stackedPages.setCurrentWidget(self.ui.pageAI)

    def manual(self):
        self.ui.stackedPages.setCurrentWidget(self.ui.pageManual)

    def leaderboard(self):
        self.ui.stackedPages.setCurrentWidget(self.ui.pageBoard)

    def update_leaderboard(self, players):
        if players:
            name_labels = [getattr(self.ui, f"name{i}") for i in range(1, 11)]
            pickup_labels = [getattr(self.ui, f"pickups{i}") for i in range(1, 11)]

            for i, p in enumerate(players[:10]):
                name_labels[i].setText(p['name'])
                pickup_labels[i].setText(f"{p['score']} pickups")

    def start_interaction(self):
        self.ui.stackedLogin.setCurrentWidget(self.interactionui.get_widget())
        self.interactionui.startup()

    def end_interaction(self):
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
