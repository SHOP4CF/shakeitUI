import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit
from MainUI import Ui_MainWindow
import requests
import base64
import json


class MainWindow:
    def __init__(self):
        # setting up KeyRock #

        # create subject token
        url = "https://localhost:443/v1/auth/tokens"
        data = {'name': 'admin@test.com', 'password': '1234'}
        head = {'Content-Type': 'application/json'}
        r = requests.post(url, json=data, headers=head, verify=False)
        subjectToken = r.headers['X-Subject-Token']

        # register application in keyrock
        url = "https://localhost:443/v1/applications"
        payload = json.dumps({
            "application": {
                "name": "Test_application 1",
                "description": "description",
                "redirect_uri": "http://localhost/login",
                "redirect_sign_out_uri": "http://localhost/logout",
                "url": "http://localhost",
                "grant_type": [
                    "authorization_code",
                    "implicit",
                    "password"
                ],
                "token_types": [
                    "jwt",
                    "permanent"
                ]
            }
        })
        headers = {
            'Content-Type': 'application/json',
            'X-Auth-token': subjectToken
        }

        response = requests.request("POST", url, headers=headers, data=payload, verify=False)

        # Base 64 encoding client info
        clientID = response.json()['application']['id']
        clientSecret = response.json()['application']['secret']
        clientInfo = clientID + ":" + clientSecret
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

        # connecting buttons
        self.ui.buttonLogin.clicked.connect(self.login)
        self.ui.buttonLogout.clicked.connect(self.logout)

        # connecting radiobuttons
        self.ui.radioAI.toggled.connect(self.ai)
        self.ui.radioManual.toggled.connect(self.manual)
        self.ui.radioVS.toggled.connect(self.vs)

    def show(self):
        self.main_win.show()

    def login(self):
        username = self.ui.textUsername.text()
        password = self.ui.textPassword.text()

        url = "https://localhost:443/oauth2/token"
        d = {'username': username,
             'password': password,
             'grant_type': 'password'}
        h = {'Accept': 'application/json',
             'Authorization': 'Basic ' + self.clientInfoBase64,
             'Content-Type': 'application/x-www-form-urlencoded'}

        r = requests.post(url, data=d, headers=h, verify=False)

        if r.status_code == 200:
            # success
            print("access token: " + json.loads(r.text)['access_token'])

            self.ui.stackedLogin.setCurrentWidget(self.ui.mainPage)
            self.ui.stackedPages.setCurrentWidget(self.ui.pageAI)
            self.ui.radioAI.toggle()
            self.ui.textPassword.clear()
            self.ui.textUsername.clear()
            self.ui.labelLoginError.hide()

        elif r.status_code == 400:
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

    def vs(self):
        self.ui.stackedPages.setCurrentWidget(self.ui.pageVS)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())
