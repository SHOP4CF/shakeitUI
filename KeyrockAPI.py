import requests
import base64
import json


class KeyrockAPI:

    def __init__(self):
        # GET CLIENT INFO #
        self.application = json.loads(open('applicationInfo.json').read())

        # Base 64 encoding client info
        clientInfo = self.application["clientID"] + ":" + self.application["clientSecret"]
        clientInfoBytes = clientInfo.encode("ascii")
        clientInfoBytesBase64 = base64.b64encode(clientInfoBytes)
        self.clientInfoBase64 = clientInfoBytesBase64.decode("ascii")

    def createSubjectToken(self):
        url = "https://localhost:443/v1/auth/tokens"
        data = {'name': self.application["adminUsername"], 'password': self.application["adminPassword"]}
        head = {'Content-Type': 'application/json'}
        r = requests.post(url, json=data, headers=head, verify=False)

        return r.headers['X-Subject-Token']

    def getAuthorizedUsers(self):
        # List of Authorized users
        url = "https://localhost:443/v1/applications/{}/users".format(self.application["clientID"])
        h = {'x-Auth-token': self.createSubjectToken()}
        rUsers = requests.get(url, headers=h, verify=False)

        users = json.loads(rUsers.content)['role_user_assignments']

        userIDs = []
        for user in users:
            userIDs.append(user['user_id'])

        return userIDs

    def authenticateUser(self, username, password):
        url = "https://localhost:443/oauth2/token"
        d = {'username': username,
             'password': password,
             'grant_type': 'password'}
        h = {'Accept': 'application/json',
             'Authorization': 'Basic ' + self.clientInfoBase64,
             'Content-Type': 'application/x-www-form-urlencoded'}
        rAuth = requests.post(url, data=d, headers=h, verify=False)
        accessToken = json.loads(rAuth.text)['access_token']

        if rAuth.status_code == 200:
            # check if user is authorized in application
            if self.getUserInfo(accessToken)['id'] in self.getAuthorizedUsers():
                return True, accessToken
            else:
                return False, None
        else:
            return False, None

    def getUserInfo(self, aToken):
        url = "https://localhost:443/user?access_token=" + aToken
        rUserInfo = requests.get(url, verify=False)
        return json.loads(rUserInfo.text)
