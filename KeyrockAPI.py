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

    def authenticateUser(self, username, password, user):
        url = "https://localhost:443/oauth2/token"
        d = {'username': username,
             'password': password,
             'grant_type': 'password'}
        h = {'Accept': 'application/json',
             'Authorization': 'Basic ' + self.clientInfoBase64,
             'Content-Type': 'application/x-www-form-urlencoded'}
        rAuth = requests.post(url, data=d, headers=h, verify=False)

        if rAuth.status_code == 200:
            i = json.loads(rAuth.text)
            # check if user is authorized in application
            if self.getUserInfo(i['access_token'])['id'] in self.getAuthorizedUsers():
                user.updateAccess(i['access_token'], i['refresh_token'])
                return True, user
        return False, user

    def getUserInfo(self, user):
        url = "https://localhost:443/user?access_token=" + user.accessToken
        rUserInfo = requests.get(url, verify=False)
        i = json.loads(rUserInfo.text)
        user.updateInfo(i['username', i['roles'][0]['name']])
        return user

    def refreshToken(self, rToken):
        url = "https://localhost:443/oauth2/token"
        d = {'refresh_token': rToken,
             'grant_type': 'password'}
        h = {'Accept': 'application/json',
             'Authorization': 'Basic ' + self.clientInfoBase64,
             'Content-Type': 'application/x-www-form-urlencoded'}
        rRefreshToken = requests.post(url, data=d, headers=h, verify=False)
        newAccessToken = json.loads(rRefreshToken.text)['access_token']
        newRefreshToken = json.loads(rRefreshToken.text)['refresh_token']
        return newAccessToken, newRefreshToken
