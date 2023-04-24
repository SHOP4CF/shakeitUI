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

    def create_subject_token(self):
        url = "https://localhost:443/v1/auth/tokens"
        data = {'name': self.application["adminUsername"], 'password': self.application["adminPassword"]}
        head = {'Content-Type': 'application/json'}
        r = requests.post(url, json=data, headers=head, verify=False)

        return r.headers['X-Subject-Token']

    def get_authorized_users(self):
        # List of Authorized users
        url = "https://localhost:443/v1/applications/{}/users".format(self.application["clientID"])
        h = {'x-Auth-token': self.create_subject_token()}
        r_users = requests.get(url, headers=h, verify=False)

        users = json.loads(r_users.content)['role_user_assignments']

        userIDs = []
        for user in users:
            userIDs.append(user['user_id'])

        return userIDs

    def authenticate_user(self, username, password, user):
        url = "https://localhost:443/oauth2/token"
        d = {'username': username,
             'password': password,
             'grant_type': 'password'}
        h = {'Accept': 'application/json',
             'Authorization': 'Basic ' + self.clientInfoBase64,
             'Content-Type': 'application/x-www-form-urlencoded'}
        r_auth = requests.post(url, data=d, headers=h, verify=False)

        if r_auth.status_code == 200:
            i = json.loads(r_auth.text)
            # check if user is authorized in application
            user.update_access(i['access_token'], json.loads(r_auth.text)['refresh_token'])
            user = self.get_user_info(user)
            if user.id in self.get_authorized_users():
                return True, user
            else:
                return False, user
        return False, user

    def authorize_user(self, user, action, resource):
        subject_token = self.create_subject_token()

        # List of users and their roles
        url = "https://localhost:443/v1/applications/{}/users".format(self.application["clientID"])
        h = {'x-Auth-token': subject_token}
        r_users = requests.get(url, headers=h, verify=False)
        users = json.loads(r_users.content)['role_user_assignments']

        # Find the roles of the user
        roles = []
        for u in users:
            if u['user_id'] == user.id:
                roles.append(u['role_id'])

        # Find permissions of each role
        allowed_access = []
        for role in roles:
            url2 = "https://localhost:443/v1/applications/{}/roles/{}/permissions".format(self.application["clientID"], role)
            h2 = {'x-Auth-token': subject_token}
            r_permissions = requests.get(url2, headers=h2, verify=False)
            permissions = json.loads(r_permissions.content)["role_permission_assignments"]

            for permission in permissions:
                if permission['action'] is not None and permission['resource'] is not None:
                    allowed_access.append({'action': permission['action'], 'resource': permission['resource']})

        # Check if user has permission to do action on resource
        for a in allowed_access:
            if a['action'] == action and a['resource'] == resource:
                return True
        return False

    def get_user_info(self, user):
        url = "https://localhost:443/user?access_token=" + user.accessToken
        r_userinfo = requests.get(url, verify=False)
        i = json.loads(r_userinfo.text)
        try:
            user.update_info(i['username'], i['roles'][0]['name'], i['id'])
        except:
            user.update_info(i['username'], " ", i['id'])
        return user

    def refresh_token(self, user):
        url = "https://localhost:443/oauth2/token"
        d = {'refresh_token': user.refresh_token,
             'grant_type': 'refresh_token'}
        h = {'Accept': 'application/json',
             'Authorization': 'Basic ' + self.clientInfoBase64,
             'Content-Type': 'application/x-www-form-urlencoded'}
        r_refreshtoken = requests.post(url, data=d, headers=h, verify=False)

        i = json.loads(r_refreshtoken.text)
        user.update_access(i['access_token'], i['refresh_token'])
        return user
