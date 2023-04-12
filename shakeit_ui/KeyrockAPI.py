import requests
import base64
import json


class KeyrockAPI:

    def __init__(self):
        # GET CLIENT INFO #
        self.application = json.loads(open('/home/jeda/wspace/shakeit/ros_pkg_ws/src/shakeit_ui/resource/applicationInfo.json').read())

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
            user.updateAccess(i['access_token'], json.loads(rAuth.text)['refresh_token'])
            user = self.getUserInfo(user)
            if user.id in self.getAuthorizedUsers():
                return True, user
            else:
                return False, user
        return False, user

    def authorizeUser(self, user, action, resource):
        subtoken = self.createSubjectToken()

        # List of users and their roles
        url = "https://localhost:443/v1/applications/{}/users".format(self.application["clientID"])
        h = {'x-Auth-token': subtoken}
        rUsers = requests.get(url, headers=h, verify=False)
        users = json.loads(rUsers.content)['role_user_assignments']

        # Find the roles of the user
        roles = []
        for u in users:
            if u['user_id'] == user.id:
                roles.append(u['role_id'])

        # Find permissions of each role
        allowedAccess = []
        for role in roles:
            url2 = "https://localhost:443/v1/applications/{}/roles/{}/permissions".format(self.application["clientID"], role)
            h2 = {'x-Auth-token': subtoken}
            rPermission = requests.get(url2, headers=h2, verify=False)
            permissions = json.loads(rPermission.content)["role_permission_assignments"]

            for permission in permissions:
                if permission['action'] is not None and permission['resource'] is not None:
                    allowedAccess.append({'action': permission['action'], 'resource': permission['resource']})

        # Check if user has permission to do action on resource
        for a in allowedAccess:
            if a['action'] == action and a['resource'] == resource:
                return True
        return False

    def getUserInfo(self, user):
        url = "https://localhost:443/user?access_token=" + user.accessToken
        rUserInfo = requests.get(url, verify=False)
        i = json.loads(rUserInfo.text)
        try:
            user.updateInfo(i['username'], i['roles'][0]['name'], i['id'])
        except:
            user.updateInfo(i['username'], " ", i['id'])
        return user

    def refreshToken(self, user):
        url = "https://localhost:443/oauth2/token"
        d = {'refresh_token': user.refreshToken,
             'grant_type': 'refresh_token'}
        h = {'Accept': 'application/json',
             'Authorization': 'Basic ' + self.clientInfoBase64,
             'Content-Type': 'application/x-www-form-urlencoded'}
        rRefreshToken = requests.post(url, data=d, headers=h, verify=False)

        i = json.loads(rRefreshToken.text)
        user.updateAccess(i['access_token'], i['refresh_token'])
        return user
