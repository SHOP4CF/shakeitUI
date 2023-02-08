import sys
import signal
import subprocess

from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit
from shakeit_ui.MainUI import Ui_MainWindow
from shakeit_ui.Interaction import InteractionWindow
import requests
import base64
import json


class MainWindow:
    def __init__(self):
        application = json.loads(open('/home/dti/wspace/shakeit/ros_pkg_ws/src/shakeit_ui/resource/applicationInfo.json').read())

        # Base 64 encoding client info
        clientInfo = application["clientID"] + ":" + application["clientSecret"]
        clientInfoBytes = clientInfo.encode("ascii")
        clientInfoBytesBase64 = base64.b64encode(clientInfoBytes)
        self.clientInfoBase64 = clientInfoBytesBase64.decode("ascii")

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
        self.ui.buttonStart.clicked.connect(self.startSHAKEIT)
        self.ui.buttonStop.clicked.connect(self.stopSHAKEIT)

        # connecting radiobuttons
        self.ui.radioAI.toggled.connect(self.ai)
        self.ui.radioManual.toggled.connect(self.manual)
        self.ui.radioVS.toggled.connect(self.vs)
        self.ui.radioInteraction.toggled.connect(self.startInteraction)

        self.show()

    def startSHAKEIT(self):
        print("Launching SHAKEIT run_experiment!")
        self.launch_SHAKEIT = subprocess.Popen(["ros2", "launch", "shakeit_experiments", "run_experiment.launch.py"])
        print(self.launch_SHAKEIT.pid)

    def stopSHAKEIT(self):
        print("Closing SHAKEIT experiment")        
        self.launch_SHAKEIT.send_signal(signal.SIGINT)
        self.launch_SHAKEIT.wait()
        print("CTRL+C killed the process")

    def show(self):
        self.main_win.show()

    def login(self):
        username = self.ui.textUsername.text()
        password = self.ui.textPassword.text()

        # # Use KeyRock to authenticate user
        # url = "https://localhost:443/oauth2/token"
        # d = {'username': username,
        #      'password': password,
        #      'grant_type': 'password'}
        # h = {'Accept': 'application/json',
        #      'Authorization': 'Basic ' + self.clientInfoBase64,
        #      'Content-Type': 'application/x-www-form-urlencoded'}
        # rAuth = requests.post(url, data=d, headers=h, verify=False)

        # if rAuth.status_code == 200:
        #     # success
        #     aToken = json.loads(rAuth.text)['access_token']
        #     print("access token: " + aToken)

        #     # get userinfo from access token
        #     url = "https://localhost:443/user?access_token=" + aToken
        #     rUserInfo = requests.get(url, verify=False)

        #     try:
        #         self.ui.labelRole.setText(json.loads(rUserInfo.text)['roles'][0]['name'])
        #     except:
        #         self.ui.labelRole.setText("")

        #     self.ui.labelUsername_2.setText(json.loads(rUserInfo.text)['username'])

        # change to mainPage
        self.ui.stackedLogin.setCurrentWidget(self.ui.mainPage)
        self.ui.stackedPages.setCurrentWidget(self.ui.pageAI)
        self.ui.radioAI.toggle()

        #     # clear the login page
        #     self.ui.textPassword.clear()
        #     self.ui.textUsername.clear()
        #     self.ui.labelLoginError.hide()

        # elif rAuth.status_code == 400:
        #     # failure
        #     self.ui.labelLoginError.show()
        #     self.ui.textPassword.clear()
        #     self.ui.textUsername.clear()

    def logout(self):
        self.ui.stackedLogin.setCurrentWidget(self.ui.loginPage)

    def ai(self):
        self.ui.stackedPages.setCurrentWidget(self.ui.pageAI)

    def manual(self):
        self.ui.stackedPages.setCurrentWidget(self.ui.pageManual)

    def vs(self):
        self.ui.stackedPages.setCurrentWidget(self.ui.pageVS)

    def startInteraction(self):
        self.ui.stackedLogin.setCurrentWidget(self.interactionui.getWidget())
        self.interactionui.startup()

    def endInteraction(self):
        self.ui.radioVS.toggle()
        self.ui.stackedLogin.setCurrentWidget(self.ui.mainPage)
        self.ui.stackedPages.setCurrentWidget(self.ui.pageVS)

    def close_application(self):
        print("Closing the application")
        sys.exit()


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     main_win = MainWindow()
#     main_win.show()
#     sys.exit(app.exec_())
