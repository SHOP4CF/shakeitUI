
class LoggedInUser:

    def __init__(self):
        self.username = None
        self.role = None
        self.accessToken = None
        self.refreshToken = None

    def updateInfo(self, username, role):
        self.username = username
        self.role = role

    def updateAccess(self, newAccess, newRefresh):
        self.accessToken = newAccess
        self.refreshToken = newRefresh
